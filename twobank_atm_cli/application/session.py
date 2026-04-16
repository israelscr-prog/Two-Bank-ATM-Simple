# application/session.py — TWO Bank ATM
# ATMSession orquesta todos los use cases de la sesión activa.

from __future__ import annotations

import uuid
from typing import Optional

from domain.entities import Account, Card, Transaction
from domain.enums import AccountStatus, TransactionType
from domain.exceptions import (
    AccountBlockedError,
    AuthenticationError,
    CardBlockedError,
    SessionError,
)
from infrastructure.repositories import (
    InMemoryAccountRepo,
    InMemoryCardRepo,
    InMemoryTransactionRepo,
)


class ATMSession:

    def __init__(
        self,
        account_repo: InMemoryAccountRepo,
        card_repo:    InMemoryCardRepo,
        tx_repo:      InMemoryTransactionRepo,
    ):
        self.account_repo = account_repo
        self.card_repo    = card_repo
        self.tx_repo      = tx_repo
        self.current_card:    Optional[Card]    = None
        self.current_account: Optional[Account] = None

    # ─────────────────────────────────────────
    # Helper privado
    # ─────────────────────────────────────────

    def _require_session(self) -> None:
        if not self.current_card or not self.current_account:
            raise SessionError("No hay sesión activa.")

    def _record(self, tx_type: TransactionType, amount: float) -> Transaction:
        tx = Transaction(
            id=uuid.uuid4(),
            account_id=self.current_account.id,
            type=tx_type,
            amount=amount,
            currency=self.current_account.currency,
        )
        self.tx_repo.save(tx)
        self.current_account.transactions.append(tx)
        return tx

    # ─────────────────────────────────────────
    # Use Case: Authenticate
    # ─────────────────────────────────────────

    def authenticate(self, card_number: str, pin: str) -> None:
        card = self.card_repo.get_by_number(card_number)

        if card.blocked:
            raise CardBlockedError("Tarjeta bloqueada. Contacte con su banco.")
        if not card.check_pin(pin):
            raise AuthenticationError("PIN incorrecto.")

        account = self.account_repo.get_by_id(card.account_id)
        if account.status == AccountStatus.BLOCKED:
            raise AccountBlockedError("Cuenta bloqueada. Contacte con su banco.")

        self.current_card    = card
        self.current_account = account

    # ─────────────────────────────────────────
    # Use Case: Check Balance
    # ─────────────────────────────────────────

    def check_balance(self) -> str:
        self._require_session()
        acc = self.current_account
        return f"Saldo disponible: {acc.balance:.2f} {acc.currency}"

    # ─────────────────────────────────────────
    # Use Case: Withdraw
    # ─────────────────────────────────────────

    def withdraw(self, amount: float) -> str:
        self._require_session()
        acc = self.current_account
        acc.withdraw(amount)
        self._record(TransactionType.WITHDRAWAL, amount)
        return f"Retirado {amount:.2f} {acc.currency}. Nuevo saldo: {acc.balance:.2f} {acc.currency}"

    # ─────────────────────────────────────────
    # Use Case: Deposit
    # ─────────────────────────────────────────

    def deposit(self, amount: float) -> str:
        self._require_session()
        acc = self.current_account
        acc.deposit(amount)
        self._record(TransactionType.DEPOSIT, amount)
        return f"Ingresado {amount:.2f} {acc.currency}. Nuevo saldo: {acc.balance:.2f} {acc.currency}"

    # ─────────────────────────────────────────
    # Use Case: Change PIN
    # ─────────────────────────────────────────

    def change_pin(self, old_pin: str, new_pin: str) -> str:
        self._require_session()
        self.current_card.change_pin(old_pin, new_pin)
        return "✅ PIN cambiado correctamente."

    # ─────────────────────────────────────────
    # Use Case: Mini Statement
    # ─────────────────────────────────────────

    def mini_statement(self) -> str:
        self._require_session()
        txs = self.tx_repo.get_by_account(self.current_account.id, limit=5)
        if not txs:
            return "No hay movimientos recientes."
        lines = ["─" * 44, f"  Últimos movimientos — {self.current_account.owner}", "─" * 44]
        for tx in txs:
            lines.append(f"  {tx}")
        lines.append("─" * 44)
        return "\n".join(lines)

    # ─────────────────────────────────────────
    # Logout
    # ─────────────────────────────────────────

    def logout(self) -> None:
        self.current_card    = None
        self.current_account = None
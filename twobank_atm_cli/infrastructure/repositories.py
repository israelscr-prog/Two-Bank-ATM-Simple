# infrastructure/repositories.py — TWO Bank ATM
# Repositorios en memoria: simulan una base de datos durante la sesión.

from __future__ import annotations

import uuid

from domain.entities import Account, Card, Transaction
from domain.exceptions import NotFoundError


# ─────────────────────────────────────────
# Account Repository
# ─────────────────────────────────────────

class InMemoryAccountRepo:

    def __init__(self):
        self._data: dict[uuid.UUID, Account] = {}

    def save(self, account: Account) -> None:
        self._data[account.id] = account

    def get_by_id(self, account_id: uuid.UUID) -> Account:
        account = self._data.get(account_id)
        if not account:
            raise NotFoundError(f"Cuenta {account_id} no encontrada.")
        return account


# ─────────────────────────────────────────
# Card Repository
# ─────────────────────────────────────────

class InMemoryCardRepo:

    def __init__(self):
        self._data: dict[str, Card] = {}   # key = número de tarjeta

    def save(self, card: Card) -> None:
        self._data[card.number] = card

    def get_by_number(self, number: str) -> Card:
        card = self._data.get(number)
        if not card:
            raise NotFoundError(f"Tarjeta {number} no encontrada.")
        return card


# ─────────────────────────────────────────
# Transaction Repository
# ─────────────────────────────────────────

class InMemoryTransactionRepo:

    def __init__(self):
        self._data: list[Transaction] = []

    def save(self, tx: Transaction) -> None:
        self._data.append(tx)

    def get_by_account(self, account_id: uuid.UUID, limit: int = 5) -> list[Transaction]:
        recent = [t for t in reversed(self._data) if t.account_id == account_id]
        return recent[:limit]
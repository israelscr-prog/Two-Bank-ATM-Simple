# domain/entities.py — TWO Bank ATM
# Entidades del dominio: Account, Card, Transaction

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from domain.enums import AccountStatus, TransactionType
from domain.exceptions import (
    AccountBlockedError,
    AuthenticationError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidPinError,
)


# ─────────────────────────────────────────
# Helper
# ─────────────────────────────────────────

def hash_pin(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


# ─────────────────────────────────────────
# Transaction
# ─────────────────────────────────────────

@dataclass
class Transaction:
    id:         uuid.UUID
    account_id: uuid.UUID
    type:       TransactionType
    amount:     float
    currency:   str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __str__(self) -> str:
        ts = self.created_at.strftime("%d/%m/%Y %H:%M")
        return f"[{ts}]  {self.type.value:12s}  {self.amount:>10.2f} {self.currency}"


# ─────────────────────────────────────────
# Account
# ─────────────────────────────────────────

@dataclass
class Account:
    id:           uuid.UUID
    owner:        str
    balance:      float
    currency:     str
    status:       AccountStatus = AccountStatus.ACTIVE
    transactions: list[Transaction] = field(default_factory=list)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("El importe debe ser mayor que 0.")
        if self.status == AccountStatus.BLOCKED:
            raise AccountBlockedError("La cuenta está bloqueada.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("El importe debe ser mayor que 0.")
        if self.status == AccountStatus.BLOCKED:
            raise AccountBlockedError("La cuenta está bloqueada.")
        if amount > self.balance:
            raise InsufficientFundsError("Saldo insuficiente.")
        self.balance -= amount


# ─────────────────────────────────────────
# Card
# ─────────────────────────────────────────

@dataclass
class Card:
    id:         uuid.UUID
    number:     str
    pin_hash:   str
    account_id: uuid.UUID
    blocked:    bool = False

    def check_pin(self, raw_pin: str) -> bool:
        return self.pin_hash == hash_pin(raw_pin)

    def change_pin(self, old_pin: str, new_pin: str) -> None:
        if not self.check_pin(old_pin):
            raise AuthenticationError("PIN actual incorrecto.")
        if len(new_pin) != 4 or not new_pin.isdigit():
            raise InvalidPinError("El nuevo PIN debe tener exactamente 4 dígitos.")
        self.pin_hash = hash_pin(new_pin)
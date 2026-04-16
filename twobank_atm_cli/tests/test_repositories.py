# tests/test_repositories.py — TWO Bank ATM
# Tests unitarios para los repositorios en memoria.

import uuid
import pytest

from domain.entities import Account, Card, hash_pin
from domain.enums import AccountStatus, TransactionType
from domain.entities import Transaction
from domain.exceptions import NotFoundError
from infrastructure.repositories import (
    InMemoryAccountRepo,
    InMemoryCardRepo,
    InMemoryTransactionRepo,
)
from datetime import datetime, timezone


# ─────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────

@pytest.fixture
def account():
    return Account(
        id=uuid.uuid4(),
        owner="Ana García",
        balance=1000.00,
        currency="EUR",
    )

@pytest.fixture
def card(account):
    return Card(
        id=uuid.uuid4(),
        number="1234",
        pin_hash=hash_pin("1111"),
        account_id=account.id,
    )

@pytest.fixture
def transaction(account):
    return Transaction(
        id=uuid.uuid4(),
        account_id=account.id,
        type=TransactionType.WITHDRAWAL,
        amount=100.00,
        currency="EUR",
    )


# ─────────────────────────────────────────
# InMemoryAccountRepo tests
# ─────────────────────────────────────────

class TestInMemoryAccountRepo:

    def test_save_and_get_by_id(self, account):
        repo = InMemoryAccountRepo()
        repo.save(account)
        result = repo.get_by_id(account.id)
        assert result == account

    def test_get_by_id_not_found(self):
        repo = InMemoryAccountRepo()
        with pytest.raises(NotFoundError):
            repo.get_by_id(uuid.uuid4())

    def test_save_overwrites_existing(self, account):
        repo = InMemoryAccountRepo()
        repo.save(account)
        account.balance = 9999.00
        repo.save(account)
        result = repo.get_by_id(account.id)
        assert result.balance == 9999.00


# ─────────────────────────────────────────
# InMemoryCardRepo tests
# ─────────────────────────────────────────

class TestInMemoryCardRepo:

    def test_save_and_get_by_number(self, card):
        repo = InMemoryCardRepo()
        repo.save(card)
        result = repo.get_by_number("1234")
        assert result == card

    def test_get_by_number_not_found(self):
        repo = InMemoryCardRepo()
        with pytest.raises(NotFoundError):
            repo.get_by_number("9999")

    def test_save_two_cards(self, account):
        repo = InMemoryCardRepo()
        card1 = Card(id=uuid.uuid4(), number="1111", pin_hash=hash_pin("0000"), account_id=account.id)
        card2 = Card(id=uuid.uuid4(), number="2222", pin_hash=hash_pin("0000"), account_id=account.id)
        repo.save(card1)
        repo.save(card2)
        assert repo.get_by_number("1111") == card1
        assert repo.get_by_number("2222") == card2


# ─────────────────────────────────────────
# InMemoryTransactionRepo tests
# ─────────────────────────────────────────

class TestInMemoryTransactionRepo:

    def test_save_and_get_by_account(self, transaction, account):
        repo = InMemoryTransactionRepo()
        repo.save(transaction)
        results = repo.get_by_account(account.id)
        assert len(results) == 1
        assert results[0] == transaction

    def test_get_by_account_empty(self):
        repo = InMemoryTransactionRepo()
        results = repo.get_by_account(uuid.uuid4())
        assert results == []

    def test_get_by_account_limit(self, account):
        repo = InMemoryTransactionRepo()
        for _ in range(10):
            repo.save(Transaction(
                id=uuid.uuid4(),
                account_id=account.id,
                type=TransactionType.DEPOSIT,
                amount=50.00,
                currency="EUR",
            ))
        results = repo.get_by_account(account.id, limit=5)
        assert len(results) == 5

    def test_get_by_account_returns_most_recent_first(self, account):
        repo = InMemoryTransactionRepo()
        tx1 = Transaction(id=uuid.uuid4(), account_id=account.id, type=TransactionType.DEPOSIT,    amount=100.00, currency="EUR")
        tx2 = Transaction(id=uuid.uuid4(), account_id=account.id, type=TransactionType.WITHDRAWAL, amount=200.00, currency="EUR")
        repo.save(tx1)
        repo.save(tx2)
        results = repo.get_by_account(account.id)
        assert results[0] == tx2  # más reciente primero
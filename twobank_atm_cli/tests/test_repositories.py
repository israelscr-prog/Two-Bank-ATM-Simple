# tests/test_repositories.py — TWO Bank ATM
# Tests unitarios de los repositorios en memoria.

import uuid
import pytest

from domain.entities import Account, Card, Transaction, hash_pin
from domain.enums import AccountStatus, TransactionType
from domain.exceptions import NotFoundError
from infrastructure.repositories import (
    InMemoryAccountRepo,
    InMemoryCardRepo,
    InMemoryTransactionRepo,
)
from datetime import datetime, timezone


# ─────────────────────────────────────────
# Helpers / Factories
# ─────────────────────────────────────────

def make_account(balance=500.0):
    return Account(
        id=uuid.uuid4(),
        owner="Ana García",
        balance=balance,
        currency="EUR",
        status=AccountStatus.ACTIVE,
    )


def make_card(account_id=None):
    return Card(
        id=uuid.uuid4(),
        number="1111222233334444",
        pin_hash=hash_pin("1234"),
        account_id=account_id or uuid.uuid4(),
    )


def make_tx(account_id=None, amount=100.0):
    return Transaction(
        id=uuid.uuid4(),
        account_id=account_id or uuid.uuid4(),
        type=TransactionType.DEPOSIT,
        amount=amount,
        currency="EUR",
        created_at=datetime.now(timezone.utc),
    )


# ─────────────────────────────────────────
# InMemoryAccountRepo
# ─────────────────────────────────────────

class TestInMemoryAccountRepo:

    def test_save_and_get_by_id(self):
        repo = InMemoryAccountRepo()
        account = make_account()
        repo.save(account)
        result = repo.get_by_id(account.id)
        assert result == account

    def test_save_overwrites_existing(self):
        repo = InMemoryAccountRepo()
        account = make_account(balance=100.0)
        repo.save(account)
        account.balance = 999.0
        repo.save(account)
        assert repo.get_by_id(account.id).balance == 999.0

    def test_get_by_id_not_found_raises(self):
        repo = InMemoryAccountRepo()
        with pytest.raises(NotFoundError):
            repo.get_by_id(uuid.uuid4())

    def test_save_multiple_accounts(self):
        repo = InMemoryAccountRepo()
        a1 = make_account()
        a2 = make_account()
        repo.save(a1)
        repo.save(a2)
        assert repo.get_by_id(a1.id) == a1
        assert repo.get_by_id(a2.id) == a2


# ─────────────────────────────────────────
# InMemoryCardRepo
# ─────────────────────────────────────────

class TestInMemoryCardRepo:

    def test_save_and_get_by_number(self):
        repo = InMemoryCardRepo()
        card = make_card()
        repo.save(card)
        result = repo.get_by_number(card.number)
        assert result == card

    def test_save_overwrites_existing(self):
        repo = InMemoryCardRepo()
        card = make_card()
        repo.save(card)
        card.blocked = True
        repo.save(card)
        assert repo.get_by_number(card.number).blocked is True

    def test_get_by_number_not_found_raises(self):
        repo = InMemoryCardRepo()
        with pytest.raises(NotFoundError):
            repo.get_by_number("9999000011112222")

    def test_save_multiple_cards(self):
        repo = InMemoryCardRepo()
        c1 = make_card()
        c1.number = "1111000011110000"
        c2 = make_card()
        c2.number = "2222000022220000"
        repo.save(c1)
        repo.save(c2)
        assert repo.get_by_number(c1.number) == c1
        assert repo.get_by_number(c2.number) == c2


# ─────────────────────────────────────────
# InMemoryTransactionRepo
# ─────────────────────────────────────────

class TestInMemoryTransactionRepo:

    def test_save_and_get_by_account(self):
        repo = InMemoryTransactionRepo()
        account_id = uuid.uuid4()
        tx = make_tx(account_id=account_id)
        repo.save(tx)
        result = repo.get_by_account(account_id)
        assert tx in result

    def test_get_by_account_returns_only_own_transactions(self):
        repo = InMemoryTransactionRepo()
        id1 = uuid.uuid4()
        id2 = uuid.uuid4()
        tx1 = make_tx(account_id=id1)
        tx2 = make_tx(account_id=id2)
        repo.save(tx1)
        repo.save(tx2)
        result = repo.get_by_account(id1)
        assert tx1 in result
        assert tx2 not in result

    def test_get_by_account_respects_limit(self):
        repo = InMemoryTransactionRepo()
        account_id = uuid.uuid4()
        for _ in range(10):
            repo.save(make_tx(account_id=account_id))
        result = repo.get_by_account(account_id, limit=5)
        assert len(result) == 5

    def test_get_by_account_returns_most_recent_first(self):
        repo = InMemoryTransactionRepo()
        account_id = uuid.uuid4()
        tx1 = make_tx(account_id=account_id, amount=100.0)
        tx2 = make_tx(account_id=account_id, amount=200.0)
        tx3 = make_tx(account_id=account_id, amount=300.0)
        repo.save(tx1)
        repo.save(tx2)
        repo.save(tx3)
        result = repo.get_by_account(account_id)
        assert result[0].amount == 300.0
        assert result[1].amount == 200.0
        assert result[2].amount == 100.0

    def test_get_by_account_empty_returns_empty_list(self):
        repo = InMemoryTransactionRepo()
        result = repo.get_by_account(uuid.uuid4())
        assert result == []

    def test_save_multiple_transactions(self):
        repo = InMemoryTransactionRepo()
        account_id = uuid.uuid4()
        tx1 = make_tx(account_id=account_id, amount=50.0)
        tx2 = make_tx(account_id=account_id, amount=75.0)
        repo.save(tx1)
        repo.save(tx2)
        result = repo.get_by_account(account_id)
        assert len(result) == 2
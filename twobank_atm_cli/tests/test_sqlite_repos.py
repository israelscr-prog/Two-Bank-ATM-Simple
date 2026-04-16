# tests/test_sqlite_repos.py — TWO Bank ATM
# Tests de integración para los repositorios SQLite.

import uuid
import pytest

from domain.entities import Account, Card, Transaction, hash_pin
from domain.enums import AccountStatus, TransactionType
from domain.exceptions import NotFoundError
from infrastructure.sqlite.database import init_db, get_connection
from infrastructure.sqlite.sqlite_account_repo import SQLiteAccountRepo
from infrastructure.sqlite.sqlite_card_repo import SQLiteCardRepo
from infrastructure.sqlite.sqlite_transaction_repo import SQLiteTransactionRepo


# ─────────────────────────────────────────
# Setup — DB en memoria para tests
# ─────────────────────────────────────────

@pytest.fixture(autouse=True)
def clean_db(monkeypatch):
    """Usa una DB en memoria limpia para cada test."""
    import sqlite3
    import infrastructure.sqlite.database as db_module

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    get_conn = lambda: conn
    monkeypatch.setattr(db_module, "get_connection", get_conn)
    monkeypatch.setattr("infrastructure.sqlite.sqlite_account_repo.get_connection",    get_conn)
    monkeypatch.setattr("infrastructure.sqlite.sqlite_card_repo.get_connection",       get_conn)
    monkeypatch.setattr("infrastructure.sqlite.sqlite_transaction_repo.get_connection", get_conn)

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS accounts (
            id        TEXT PRIMARY KEY,
            owner     TEXT NOT NULL,
            balance   REAL NOT NULL,
            currency  TEXT NOT NULL,
            status    TEXT NOT NULL DEFAULT 'ACTIVE'
        );
        CREATE TABLE IF NOT EXISTS cards (
            id         TEXT PRIMARY KEY,
            number     TEXT UNIQUE NOT NULL,
            pin_hash   TEXT NOT NULL,
            account_id TEXT NOT NULL,
            blocked    INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        );
        CREATE TABLE IF NOT EXISTS transactions (
            id         TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
            type       TEXT NOT NULL,
            amount     REAL NOT NULL,
            currency   TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        );
    """)
    yield
    conn.close()


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
def account_repo():
    return SQLiteAccountRepo()

@pytest.fixture
def card_repo():
    return SQLiteCardRepo()

@pytest.fixture
def tx_repo():
    return SQLiteTransactionRepo()


# ─────────────────────────────────────────
# SQLiteAccountRepo tests
# ─────────────────────────────────────────

class TestSQLiteAccountRepo:

    def test_save_and_get_by_id(self, account_repo, account):
        account_repo.save(account)
        result = account_repo.get_by_id(account.id)
        assert result.owner   == account.owner
        assert result.balance == account.balance
        assert result.currency == account.currency

    def test_get_by_id_not_found(self, account_repo):
        with pytest.raises(NotFoundError):
            account_repo.get_by_id(uuid.uuid4())

    def test_save_updates_balance(self, account_repo, account):
        account_repo.save(account)
        account.balance = 9999.00
        account_repo.save(account)
        result = account_repo.get_by_id(account.id)
        assert result.balance == 9999.00

    def test_save_updates_status(self, account_repo, account):
        account_repo.save(account)
        account.status = AccountStatus.BLOCKED
        account_repo.save(account)
        result = account_repo.get_by_id(account.id)
        assert result.status == AccountStatus.BLOCKED


# ─────────────────────────────────────────
# SQLiteCardRepo tests
# ─────────────────────────────────────────

class TestSQLiteCardRepo:

    def test_save_and_get_by_number(self, account_repo, card_repo, account, card):
        account_repo.save(account)
        card_repo.save(card)
        result = card_repo.get_by_number("1234")
        assert result.number   == card.number
        assert result.pin_hash == card.pin_hash

    def test_get_by_number_not_found(self, card_repo):
        with pytest.raises(NotFoundError):
            card_repo.get_by_number("9999")

    def test_save_updates_pin(self, account_repo, card_repo, account, card):
        account_repo.save(account)
        card_repo.save(card)
        card.pin_hash = hash_pin("9999")
        card_repo.save(card)
        result = card_repo.get_by_number("1234")
        assert result.check_pin("9999") is True

    def test_save_updates_blocked(self, account_repo, card_repo, account, card):
        account_repo.save(account)
        card_repo.save(card)
        card.blocked = True
        card_repo.save(card)
        result = card_repo.get_by_number("1234")
        assert result.blocked is True

    def test_foreign_key_fails_without_account(self, card_repo, card):
        import sqlite3
        with pytest.raises(sqlite3.IntegrityError):
            card_repo.save(card)


# ─────────────────────────────────────────
# SQLiteTransactionRepo tests
# ─────────────────────────────────────────

class TestSQLiteTransactionRepo:

    def test_save_and_get_by_account(self, account_repo, tx_repo, account):
        account_repo.save(account)
        tx = Transaction(
            id=uuid.uuid4(),
            account_id=account.id,
            type=TransactionType.DEPOSIT,
            amount=200.00,
            currency="EUR",
        )
        tx_repo.save(tx)
        results = tx_repo.get_by_account(account.id)
        assert len(results) == 1
        assert results[0].amount == 200.00

    def test_get_by_account_empty(self, tx_repo):
        results = tx_repo.get_by_account(uuid.uuid4())
        assert results == []

    def test_get_by_account_limit(self, account_repo, tx_repo, account):
        account_repo.save(account)
        for _ in range(10):
            tx_repo.save(Transaction(
                id=uuid.uuid4(),
                account_id=account.id,
                type=TransactionType.WITHDRAWAL,
                amount=50.00,
                currency="EUR",
            ))
        results = tx_repo.get_by_account(account.id, limit=5)
        assert len(results) == 5

    def test_get_by_account_most_recent_first(self, account_repo, tx_repo, account):
        account_repo.save(account)
        tx1 = Transaction(id=uuid.uuid4(), account_id=account.id, type=TransactionType.DEPOSIT,    amount=100.00, currency="EUR")
        tx2 = Transaction(id=uuid.uuid4(), account_id=account.id, type=TransactionType.WITHDRAWAL, amount=200.00, currency="EUR")
        tx_repo.save(tx1)
        tx_repo.save(tx2)
        results = tx_repo.get_by_account(account.id)
        assert results[0].amount == 200.00
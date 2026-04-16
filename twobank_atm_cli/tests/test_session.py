# tests/test_session.py — TWO Bank ATM
# Tests unitarios para ATMSession (use cases).

import uuid
import pytest

from domain.entities import Account, Card, hash_pin
from domain.enums import AccountStatus
from domain.exceptions import (
    AccountBlockedError,
    AuthenticationError,
    CardBlockedError,
    InsufficientFundsError,
    SessionError,
    NotFoundError,
)
from application.session import ATMSession
from infrastructure.repositories import (
    InMemoryAccountRepo,
    InMemoryCardRepo,
    InMemoryTransactionRepo,
)


# ─────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────

@pytest.fixture
def repos():
    return (
        InMemoryAccountRepo(),
        InMemoryCardRepo(),
        InMemoryTransactionRepo(),
    )

@pytest.fixture
def setup(repos):
    account_repo, card_repo, tx_repo = repos

    account = Account(
        id=uuid.uuid4(),
        owner="Ana García",
        balance=1000.00,
        currency="EUR",
    )
    card = Card(
        id=uuid.uuid4(),
        number="1234",
        pin_hash=hash_pin("1111"),
        account_id=account.id,
    )
    account_repo.save(account)
    card_repo.save(card)

    session = ATMSession(account_repo, card_repo, tx_repo)
    return session, account, card


# ─────────────────────────────────────────
# Authenticate tests
# ─────────────────────────────────────────

class TestAuthenticate:

    def test_login_success(self, setup):
        session, _, _ = setup
        session.authenticate("1234", "1111")
        assert session.current_account is not None
        assert session.current_card is not None

    def test_login_wrong_pin(self, setup):
        session, _, _ = setup
        with pytest.raises(AuthenticationError):
            session.authenticate("1234", "9999")

    def test_login_card_not_found(self, setup):
        session, _, _ = setup
        with pytest.raises(NotFoundError):
            session.authenticate("9999", "1111")

    def test_login_blocked_card(self, setup):
        session, _, card = setup
        card.blocked = True
        with pytest.raises(CardBlockedError):
            session.authenticate("1234", "1111")

    def test_login_blocked_account(self, setup):
        session, account, _ = setup
        account.status = AccountStatus.BLOCKED
        with pytest.raises(AccountBlockedError):
            session.authenticate("1234", "1111")


# ─────────────────────────────────────────
# Check Balance tests
# ─────────────────────────────────────────

class TestCheckBalance:

    def test_check_balance_success(self, setup):
        session, _, _ = setup
        session.authenticate("1234", "1111")
        result = session.check_balance()
        assert "1000.00" in result
        assert "EUR" in result

    def test_check_balance_no_session(self, setup):
        session, _, _ = setup
        with pytest.raises(SessionError):
            session.check_balance()


# ─────────────────────────────────────────
# Withdraw tests
# ─────────────────────────────────────────

class TestWithdraw:

    def test_withdraw_success(self, setup):
        session, account, _ = setup
        session.authenticate("1234", "1111")
        session.withdraw(200.00)
        assert account.balance == 800.00

    def test_withdraw_insufficient_funds(self, setup):
        session, _, _ = setup
        session.authenticate("1234", "1111")
        with pytest.raises(InsufficientFundsError):
            session.withdraw(9999.00)

    def test_withdraw_records_transaction(self, setup):
        session, account, _ = setup
        account_repo, _, tx_repo = (
            session.account_repo, session.card_repo, session.tx_repo
        )
        session.authenticate("1234", "1111")
        session.withdraw(100.00)
        txs = tx_repo.get_by_account(account.id)
        assert len(txs) == 1
        assert txs[0].amount == 100.00

    def test_withdraw_no_session(self, setup):
        session, _, _ = setup
        with pytest.raises(SessionError):
            session.withdraw(100.00)


# ─────────────────────────────────────────
# Deposit tests
# ─────────────────────────────────────────

class TestDeposit:

    def test_deposit_success(self, setup):
        session, account, _ = setup
        session.authenticate("1234", "1111")
        session.deposit(500.00)
        assert account.balance == 1500.00

    def test_deposit_records_transaction(self, setup):
        session, account, _ = setup
        session.authenticate("1234", "1111")
        session.deposit(300.00)
        txs = session.tx_repo.get_by_account(account.id)
        assert len(txs) == 1
        assert txs[0].amount == 300.00

    def test_deposit_no_session(self, setup):
        session, _, _ = setup
        with pytest.raises(SessionError):
            session.deposit(100.00)


# ─────────────────────────────────────────
# Change PIN tests
# ─────────────────────────────────────────

class TestChangePin:

    def test_change_pin_success(self, setup):
        session, _, card = setup
        session.authenticate("1234", "1111")
        session.change_pin("1111", "2222")
        assert card.check_pin("2222") is True

    def test_change_pin_wrong_old(self, setup):
        session, _, _ = setup
        session.authenticate("1234", "1111")
        with pytest.raises(AuthenticationError):
            session.change_pin("9999", "2222")

    def test_change_pin_no_session(self, setup):
        session, _, _ = setup
        with pytest.raises(SessionError):
            session.change_pin("1111", "2222")


# ─────────────────────────────────────────
# Mini Statement tests
# ─────────────────────────────────────────

class TestMiniStatement:

    def test_mini_statement_empty(self, setup):
        session, _, _ = setup
        session.authenticate("1234", "1111")
        result = session.mini_statement()
        assert "No hay movimientos" in result

    def test_mini_statement_shows_transactions(self, setup):
        session, _, _ = setup
        session.authenticate("1234", "1111")
        session.withdraw(100.00)
        session.deposit(200.00)
        result = session.mini_statement()
        assert "WITHDRAWAL" in result
        assert "DEPOSIT" in result

    def test_mini_statement_no_session(self, setup):
        session, _, _ = setup
        with pytest.raises(SessionError):
            session.mini_statement()


# ─────────────────────────────────────────
# Logout tests
# ─────────────────────────────────────────

class TestLogout:

    def test_logout_clears_session(self, setup):
        session, _, _ = setup
        session.authenticate("1234", "1111")
        session.logout()
        assert session.current_card is None
        assert session.current_account is None
# tests/test_domain.py — TWO Bank ATM
# Tests unitarios de entidades y session (sin GUI, sin repos reales).

import uuid
import pytest
from unittest.mock import MagicMock

from domain.entities import Account, Card, hash_pin
from domain.enums import AccountStatus
from domain.exceptions import (
    AccountBlockedError,
    AuthenticationError,
    CardBlockedError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidPinError,
    SessionError,
)
from application.session import ATMSession


# ─────────────────────────────────────────
# Helpers / Factories
# ─────────────────────────────────────────

def make_account(balance=1000.0, status=AccountStatus.ACTIVE):
    return Account(
        id=uuid.uuid4(),
        owner="Ana García",
        balance=balance,
        currency="EUR",
        status=status,
    )


def make_card(account_id=None, pin="1234", blocked=False):
    return Card(
        id=uuid.uuid4(),
        number="0000111122223333",
        pin_hash=hash_pin(pin),
        account_id=account_id or uuid.uuid4(),
        blocked=blocked,
    )


def make_session(account=None, card=None):
    """ATMSession con repos mockeados y sesión ya autenticada."""
    account = account or make_account()
    card = card or make_card(account_id=account.id)

    account_repo = MagicMock()
    card_repo = MagicMock()
    tx_repo = MagicMock()
    tx_repo.get_by_account.return_value = []

    session = ATMSession(account_repo, card_repo, tx_repo)
    session.current_account = account
    session.current_card = card
    return session


# ─────────────────────────────────────────
# Account — deposit
# ─────────────────────────────────────────

class TestAccountDeposit:

    def test_deposit_increases_balance(self):
        acc = make_account(balance=500.0)
        acc.deposit(200.0)
        assert acc.balance == 700.0

    def test_deposit_zero_raises(self):
        acc = make_account()
        with pytest.raises(InvalidAmountError):
            acc.deposit(0)

    def test_deposit_negative_raises(self):
        acc = make_account()
        with pytest.raises(InvalidAmountError):
            acc.deposit(-50.0)

    def test_deposit_blocked_account_raises(self):
        acc = make_account(status=AccountStatus.BLOCKED)
        with pytest.raises(AccountBlockedError):
            acc.deposit(100.0)


# ─────────────────────────────────────────
# Account — withdraw
# ─────────────────────────────────────────

class TestAccountWithdraw:

    def test_withdraw_decreases_balance(self):
        acc = make_account(balance=1000.0)
        acc.withdraw(300.0)
        assert acc.balance == 700.0

    def test_withdraw_zero_raises(self):
        acc = make_account()
        with pytest.raises(InvalidAmountError):
            acc.withdraw(0)

    def test_withdraw_negative_raises(self):
        acc = make_account()
        with pytest.raises(InvalidAmountError):
            acc.withdraw(-100.0)

    def test_withdraw_insufficient_funds_raises(self):
        acc = make_account(balance=100.0)
        with pytest.raises(InsufficientFundsError):
            acc.withdraw(500.0)

    def test_withdraw_exact_balance_succeeds(self):
        acc = make_account(balance=100.0)
        acc.withdraw(100.0)
        assert acc.balance == 0.0

    def test_withdraw_blocked_account_raises(self):
        acc = make_account(status=AccountStatus.BLOCKED)
        with pytest.raises(AccountBlockedError):
            acc.withdraw(100.0)


# ─────────────────────────────────────────
# Card — check_pin / change_pin
# ─────────────────────────────────────────

class TestCard:

    def test_check_pin_correct(self):
        card = make_card(pin="1234")
        assert card.check_pin("1234") is True

    def test_check_pin_wrong(self):
        card = make_card(pin="1234")
        assert card.check_pin("9999") is False

    def test_change_pin_success(self):
        card = make_card(pin="1234")
        card.change_pin("1234", "5678")
        assert card.check_pin("5678") is True

    def test_change_pin_wrong_old_pin_raises(self):
        card = make_card(pin="1234")
        with pytest.raises(AuthenticationError):
            card.change_pin("9999", "5678")

    def test_change_pin_invalid_format_raises(self):
        card = make_card(pin="1234")
        with pytest.raises(InvalidPinError):
            card.change_pin("1234", "ab12")

    def test_change_pin_too_short_raises(self):
        card = make_card(pin="1234")
        with pytest.raises(InvalidPinError):
            card.change_pin("1234", "123")


# ─────────────────────────────────────────
# ATMSession — authenticate
# ─────────────────────────────────────────

class TestATMSessionAuthenticate:

    def _make_session_with_repos(self, account, card):
        account_repo = MagicMock()
        card_repo = MagicMock()
        tx_repo = MagicMock()
        card_repo.get_by_number.return_value = card
        account_repo.get_by_id.return_value = account
        return ATMSession(account_repo, card_repo, tx_repo)

    def test_authenticate_success(self):
        account = make_account()
        card = make_card(account_id=account.id, pin="1234")
        session = self._make_session_with_repos(account, card)
        session.authenticate("0000111122223333", "1234")
        assert session.current_account == account
        assert session.current_card == card

    def test_authenticate_wrong_pin_raises(self):
        account = make_account()
        card = make_card(account_id=account.id, pin="1234")
        session = self._make_session_with_repos(account, card)
        with pytest.raises(AuthenticationError):
            session.authenticate("0000111122223333", "9999")

    def test_authenticate_blocked_card_raises(self):
        account = make_account()
        card = make_card(account_id=account.id, blocked=True)
        session = self._make_session_with_repos(account, card)
        with pytest.raises(CardBlockedError):
            session.authenticate("0000111122223333", "1234")

    def test_authenticate_blocked_account_raises(self):
        account = make_account(status=AccountStatus.BLOCKED)
        card = make_card(account_id=account.id, pin="1234")
        session = self._make_session_with_repos(account, card)
        with pytest.raises(AccountBlockedError):
            session.authenticate("0000111122223333", "1234")


# ─────────────────────────────────────────
# ATMSession — operaciones con sesión activa
# ─────────────────────────────────────────

class TestATMSessionOperations:

    def test_check_balance_returns_string(self):
        session = make_session(account=make_account(balance=500.0))
        result = session.check_balance()
        assert "500.00" in result
        assert "EUR" in result

    def test_withdraw_updates_balance(self):
        account = make_account(balance=1000.0)
        session = make_session(account=account)
        session.withdraw(200.0)
        assert account.balance == 800.0

    def test_deposit_updates_balance(self):
        account = make_account(balance=1000.0)
        session = make_session(account=account)
        session.deposit(500.0)
        assert account.balance == 1500.0

    def test_logout_clears_session(self):
        session = make_session()
        session.logout()
        assert session.current_account is None
        assert session.current_card is None

    def test_mini_statement_no_transactions(self):
        session = make_session()
        result = session.mini_statement()
        assert "No hay movimientos" in result


# ─────────────────────────────────────────
# ATMSession — sin sesión activa
# ─────────────────────────────────────────

class TestATMSessionWithoutLogin:

    def _empty_session(self):
        return ATMSession(MagicMock(), MagicMock(), MagicMock())

    def test_check_balance_without_session_raises(self):
        with pytest.raises(SessionError):
            self._empty_session().check_balance()

    def test_withdraw_without_session_raises(self):
        with pytest.raises(SessionError):
            self._empty_session().withdraw(100.0)

    def test_deposit_without_session_raises(self):
        with pytest.raises(SessionError):
            self._empty_session().deposit(100.0)

    def test_mini_statement_without_session_raises(self):
        with pytest.raises(SessionError):
            self._empty_session().mini_statement()

    def test_change_pin_without_session_raises(self):
        with pytest.raises(SessionError):
            self._empty_session().change_pin("1234", "5678")
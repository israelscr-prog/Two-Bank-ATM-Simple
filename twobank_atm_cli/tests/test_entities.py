# tests/test_entities.py — TWO Bank ATM
# Tests unitarios para las entidades del dominio.

import uuid
import pytest

from domain.entities import Account, Card, Transaction, hash_pin
from domain.enums import AccountStatus, TransactionType
from domain.exceptions import (
    AccountBlockedError,
    AuthenticationError,
    InsufficientFundsError,
    InvalidAmountError,
    InvalidPinError,
)


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


# ─────────────────────────────────────────
# Account tests
# ─────────────────────────────────────────

class TestAccount:

    def test_deposit_increases_balance(self, account):
        account.deposit(500.00)
        assert account.balance == 1500.00

    def test_withdraw_decreases_balance(self, account):
        account.withdraw(200.00)
        assert account.balance == 800.00

    def test_withdraw_exact_balance(self, account):
        account.withdraw(1000.00)
        assert account.balance == 0.00

    def test_withdraw_insufficient_funds(self, account):
        with pytest.raises(InsufficientFundsError):
            account.withdraw(9999.00)

    def test_deposit_invalid_amount(self, account):
        with pytest.raises(InvalidAmountError):
            account.deposit(0)

    def test_withdraw_invalid_amount(self, account):
        with pytest.raises(InvalidAmountError):
            account.withdraw(-50)

    def test_deposit_blocked_account(self, account):
        account.status = AccountStatus.BLOCKED
        with pytest.raises(AccountBlockedError):
            account.deposit(100)

    def test_withdraw_blocked_account(self, account):
        account.status = AccountStatus.BLOCKED
        with pytest.raises(AccountBlockedError):
            account.withdraw(100)


# ─────────────────────────────────────────
# Card tests
# ─────────────────────────────────────────

class TestCard:

    def test_correct_pin_returns_true(self, card):
        assert card.check_pin("1111") is True

    def test_wrong_pin_returns_false(self, card):
        assert card.check_pin("9999") is False

    def test_change_pin_success(self, card):
        card.change_pin("1111", "2222")
        assert card.check_pin("2222") is True

    def test_change_pin_wrong_old_pin(self, card):
        with pytest.raises(AuthenticationError):
            card.change_pin("9999", "2222")

    def test_change_pin_invalid_format(self, card):
        with pytest.raises(InvalidPinError):
            card.change_pin("1111", "abc")

    def test_change_pin_too_short(self, card):
        with pytest.raises(InvalidPinError):
            card.change_pin("1111", "12")


# ─────────────────────────────────────────
# hash_pin tests
# ─────────────────────────────────────────

class TestHashPin:

    def test_same_pin_same_hash(self):
        assert hash_pin("1234") == hash_pin("1234")

    def test_different_pins_different_hash(self):
        assert hash_pin("1234") != hash_pin("5678")
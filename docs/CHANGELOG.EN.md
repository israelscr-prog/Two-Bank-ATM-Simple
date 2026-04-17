# CHANGELOG — Two-Bank-ATM-Simple

> 🌐 [Leer en Español](./CHANGELOG.md)

All relevant project changes documented in chronological order.

---

## [0.1.0] — 2026-04-16 — Foundations

### Added
- `domain/enums.py` — `AccountStatus`, `TransactionType`, `ATMStatus`
- `domain/exceptions.py` — Domain exception hierarchy:
  - `ATMError` (base)
  - `AuthenticationError`, `CardBlockedError`, `AccountBlockedError`
  - `InsufficientFundsError`, `InvalidAmountError`, `InvalidPinError`
  - `SessionError`, `NotFoundError`
- `domain/entities.py` — Entities: `Account`, `Card`, `Transaction`, `hash_pin()`
- `infrastructure/repositories.py` — In-memory repositories:
  - `InMemoryAccountRepo`
  - `InMemoryCardRepo`
  - `InMemoryTransactionRepo`
- `infrastructure/seed.py` — Test data: Ana García (1234/1111), Luis Pérez (5678/2222)
- `requirements.txt` — `pytest`, `pytest-cov`, `ruff`
- Base folder structure: `domain/`, `application/`, `infrastructure/`, `presentation/`, `tests/`

---

## [0.2.0] — 2026-04-16 — CLI

### Added
- `presentation/cli.py` — Full command-line interface
- `application/session.py` — ATMSession with all use cases:
  - `authenticate()` — Card and PIN login
  - `check_balance()` — Balance inquiry
  - `withdraw()` — Cash withdrawal
  - `deposit()` — Cash deposit
  - `change_pin()` — PIN change
  - `mini_statement()` — Last 5 transactions
  - `logout()` — Session logout

---

## [0.3.0] — 2026-04-16 — GUI

### Added
- `presentation/gui/` — Graphical interface with CustomTkinter
- `presentation/gui/app.py` — Main window and frame navigation
- `presentation/gui/login_frame.py` — Login screen with attempt counter
- `presentation/gui/menu_frame.py` — Main menu with all operations
- `main.py` — Dual mode: `python main.py` (GUI) / `python main.py --cli` (CLI)
- `requirements.txt` — Added `customtkinter==5.2.2`

---

## [0.4.0] — 2026-04-16 — CI Pipeline

### Added
- `.github/workflows/ci.yml` — GitHub Actions pipeline
  - Python 3.12 on ubuntu-latest
  - `ruff` for code quality
  - `pytest` with test coverage

---

## [0.5.0] — 2026-04-16 — SQLite

### Added
- `infrastructure/sqlite/database.py` — SQLite connection and schema
- `infrastructure/sqlite/sqlite_account_repo.py` — Account persistence
- `infrastructure/sqlite/sqlite_card_repo.py` — Card persistence
- `infrastructure/sqlite/sqlite_transaction_repo.py` — Transaction persistence
- `main.py` — Dual mode: `--memory` / SQLite by default
- `data/` added to `.gitignore`

---

## [0.6.0] — 2026-04-16 — SQLite Tests

### Added
- `tests/test_sqlite_repos.py` — 13 integration tests for SQLite
  - `TestSQLiteAccountRepo` — save, get, update balance/status
  - `TestSQLiteCardRepo` — save, get, update pin/blocked, foreign key
  - `TestSQLiteTransactionRepo` — save, get, limit, chronological order

### Fixed
- `sqlite_card_repo.py` — `ON CONFLICT(number)` instead of `ON CONFLICT(id)`

---

## [0.7.0] — 2026-04-17 — Full Test Suite

### Added
- `tests/test_gui.py` — 13 GUI unit tests without real display
  - `TestLoginFrame`: authenticate, on_success, error, attempts, lockout after 3 fails, reset
  - `TestMenuFrame`: balance, withdraw, deposit, mini statement, logout, refresh
  - CustomTkinter Fakes (`FakeCTkFrame`, `FakeCTkEntry`, `FakeCTkTextbox`, etc.)
    to avoid Tcl/Tk dependency in headless environments

- `tests/test_domain.py` — 28 unit tests for entities and session
  - `TestAccountDeposit`: valid amount, zero, negative, blocked account
  - `TestAccountWithdraw`: valid withdrawal, zero, negative, insufficient funds, exact, blocked
  - `TestCard`: check_pin correct/incorrect, change_pin success/wrong_pin/invalid_format/too_short
  - `TestATMSessionAuthenticate`: success, wrong pin, blocked card, blocked account
  - `TestATMSessionOperations`: balance, withdraw, deposit, logout, empty mini_statement
  - `TestATMSessionWithoutLogin`: SessionError on all operations without active session

- `tests/test_repositories.py` — 14 unit tests for in-memory repositories
  - `TestInMemoryAccountRepo`: save, get_by_id, overwrite, not_found, multiple accounts
  - `TestInMemoryCardRepo`: save, get_by_number, overwrite, not_found, multiple cards
  - `TestInMemoryTransactionRepo`: save, filter by account, limit, most recent first,
    empty list, multiple transactions

### Fixed
- `ModuleNotFoundError: No module named 'customtkinter'` — installed in the correct venv
  (`twobank_atm_cli\.venv`) instead of the root venv
- `_tkinter.TclError: Can't find a usable tk.tcl` — resolved by replacing real CTk widgets
  with Fake classes before importing the frames
- `unittest.mock.InvalidSpecError: Cannot spec a Mock object` — resolved by using
  `MagicMock()` instances instead of the `MagicMock` class in patches

### Tests
- **Total: 94 tests — 94 passed, 0 failed**

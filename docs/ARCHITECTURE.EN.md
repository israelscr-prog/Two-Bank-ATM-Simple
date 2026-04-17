# Architecture — Two-Bank-ATM

> 🌐 [Leer en Español](./ARCHITECTURE..ES.md)

### This document describes the project architecture, the responsibility of each layer, folder and file.

---

# Overview

The project follows a **clean layered architecture** inspired by Robert C. Martin's _Clean Architecture_. Each layer only depends on inner layers, never the other way around. The business logic (domain) has no knowledge of the database or the user interface.

```
┌─────────────────────────────────┐
│         presentation/           │  ← GUI (CustomTkinter) + CLI
│   gui/app  gui/login  gui/menu  │
│            cli.py               │
└────────────────┬────────────────┘
                 │ usa
┌────────────────▼────────────────┐
│          application/           │  ← Use Cases
│          session.py             │
└────────────────┬────────────────┘
                 │ usa
┌────────────────▼────────────────┐
│            domain/              │  ← Core - without dependencies
│  entities  enums  exceptions    │
└────────────────┬────────────────┘
                 │ implementado por
┌────────────────▼────────────────┐
│        infrastructure/          │  ← Data Adapters 
│  repositories  sqlite/  seed    │
└─────────────────────────────────┘
```



**Key rule:** `domain/` does not import anything from `infrastructure/`, `application/` or `presentation/`.

---

## Repository root

```
Two-Bank-ATM-Simple/
├── .github/workflows/ci.yml     # CI Pipeline CI in GitHub Actions
├── docs/
│   ├── CHANGELOG.md             # Change history
│   └── ROADMAP.md               # Planned Funcionaliies
├── twobank_atm_cli/             # Main application package
├── README.md                    # General Description of proyect
├── ARCHITECTURE.md              # This Archive
├── LICENSE
└── .gitignore
```
--- 

### `.github/workflows/ci.yml`
Pipeline de integración continua que se ejecuta en cada push o pull request. Pasos: instalar dependencias → lint con ruff → ejecutar pytest. Falla el build si hay errores de lint o tests.

---

## `twobank_atm_cli/`

Application root package. Contains the source code, tests, database, and dependencies..

### `main.py`
Application entry point. Initializes the SQLite database, loads the seed data (`seed.py`) and launches the graphical interface (`ATMApp`).

### `requirements.txt`
List of project dependencies:
- `customtkinter` — modern widgets on top of Tkinter
- `pytest`, `pytest-mock`, `pytest-cov` — testing

### `data/twobank.db`
SQLite file containing the tables `accounts`, `cards`, and `transactions`. It is automatically created when `main.py` is executed if it does not exist.


---

## `domain/`

System core. No external dependencies. Contains pure business rules.

### `entities.py`
- **`Account`** — `deposit(amount)`, `withdraw(amount)`
- **`Card`** — `check_pin(raw_pin)`, `change_pin(old_pin, new_pin)`
- **`Transaction`** — immutable record of a movement
- **`hash_pin(raw)`** — SHA-256 helper

### `enums.py`
- `AccountStatus` — `ACTIVE`, `BLOCKED`
- `TransactionType` — `DEPOSIT`, `WITHDRAWAL`

### `exceptions.py`

| Exception | When raised |
|---|---|
| `ATMError` | Base for all domain exceptions |
| `AuthenticationError` | Wrong PIN or card not found |
| `CardBlockedError` | Card is blocked |
| `AccountBlockedError` | Account is blocked |
| `InsufficientFundsError` | Withdrawal exceeds balance |
| `InvalidAmountError` | Negative or zero amount |
| `InvalidPinError` | PIN format invalid |
| `SessionError` | No active session |
| `NotFoundError` | Entity not found |

---

## `application/`

### `session.py` — `ATMSession`

| Method | Description |
|---|---|
| `authenticate(card_number, pin)` | Validates card, PIN and account status |
| `check_balance()` | Returns formatted balance |
| `withdraw(amount)` | Withdraws and records transaction |
| `deposit(amount)` | Deposits and records transaction |
| `change_pin(old_pin, new_pin)` | Changes card PIN |
| `mini_statement()` | Returns last 5 transactions |
| `logout()` | Clears active session |

---

## `infrastructure/`

### `repositories.py`
In-memory repositories for dev and unit testing: `InMemoryAccountRepo`, `InMemoryCardRepo`, `InMemoryTransactionRepo`.

### `seed.py`
Loads initial test data (accounts, cards, balances) at startup.

### `sqlite/database.py`
Manages connection to `data/twobank.db` via `get_connection()`.

### `sqlite/sqlite_account_repo.py`
Persists `Account` using `INSERT OR REPLACE INTO accounts`.

### `sqlite/sqlite_card_repo.py`
Persists `Card` using `INSERT OR REPLACE INTO cards`.

### `sqlite/sqlite_transaction_repo.py`
Inserts transactions and retrieves them ordered by `created_at DESC`.

---

## `presentation/`

### `cli.py`
Terminal interface. Prompts for card and PIN, shows numbered menu, catches domain exceptions.

### `gui/app.py` — `ATMApp`
Main window. Initialises repos and session. Switches between `LoginFrame` and `MenuFrame`.

### `gui/login_frame.py` — `LoginFrame`
Login screen. Handles auth, error messages and lockout after 3 failed attempts.

### `gui/menu_frame.py` — `MenuFrame`
Main menu. Buttons for all operations plus `_ask_amount()` dialog and `refresh()`.

---

## `tests/`

**94 tests, 0 failures.**

| File | Type | What it covers |
|---|---|---|
| `test_gui.py` | Unit | GUI frames with CTk Fakes |
| `test_domain.py` | Unit | Account, Card, ATMSession, exceptions |
| `test_entities.py` | Unit | Domain entities |
| `test_session.py` | Unit | ATMSession with mocked repos |
| `test_repositories.py` | Unit | In-memory repositories |
| `test_sqlite_repos.py` | Integration | SQLite repos with `:memory:` DB |

### Strategy
- **Unit** — `MagicMock` or in-memory repos to isolate components.
- **Integration** — real SQLite `:memory:` DB per test via `clean_db` fixture.
- **GUI** — `Fake*` classes replace CTk widgets to avoid Tcl/Tk dependency.
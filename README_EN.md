# Two-Bank-ATM

> 🌐 [Leer en Español](./README.ES.md)

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Tests](https://img.shields.io/badge/tests-94%20passed-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

ATM simulator for two banks, built in Python with **clean layered architecture**. Features a graphical interface (CustomTkinter), a command-line interface (CLI), SQLite persistence and a full test suite with 94 tests.

---

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)
- [Documentation](#documentation)
- [License](#license)

---

## Features

- 🔐 Authentication with card number and PIN (SHA-256 hashing)
- 💰 Balance inquiry, cash withdrawal and deposit
- 📋 Mini statement of the last 5 transactions
- 🔑 PIN change with format validation
- 🔒 Automatic lockout after 3 failed attempts
- 🖥️ Graphical interface with CustomTkinter (dark mode)
- 💻 Command-line interface (CLI)
- 🗄️ Data persistence with SQLite
- ✅ 94 unit and integration tests — 0 failures

---

## Technologies

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14 | Main language |
| CustomTkinter | 5.x | Graphical interface |
| SQLite | built-in | Data persistence |
| pytest | 8.x | Testing framework |
| pytest-mock | 3.x | Mocking in tests |
| pytest-cov | 6.x | Test coverage |

---

## Project Structure

Two-Bank-ATM-Simple/
├── .github/
│ └── workflows/
│ └── ci.yml # CI pipeline (lint + tests)
├── docs/
│ ├── CHANGELOG.md
│ └── ROADMAP.md
├── twobank_atm_cli/
│ ├── main.py # Entry point
│ ├── requirements.txt
│ ├── application/
│ │ └── session.py # Use cases (ATMSession)
│ ├── domain/
│ │ ├── entities.py # Account, Card, Transaction
│ │ ├── enums.py # AccountStatus, TransactionType
│ │ └── exceptions.py # Domain exceptions
│ ├── infrastructure/
│ │ ├── repositories.py # In-memory repositories
│ │ ├── seed.py # Initial data
│ │ └── sqlite/
│ │ ├── database.py
│ │ ├── sqlite_account_repo.py
│ │ ├── sqlite_card_repo.py
│ │ └── sqlite_transaction_repo.py
│ ├── presentation/
│ │ ├── cli.py # CLI interface
│ │ └── gui/
│ │ ├── app.py # Main window
│ │ ├── login_frame.py # Login screen
│ │ └── menu_frame.py # Main menu
│ └── tests/
│ ├── test_gui.py # GUI tests (13)
│ ├── test_domain.py # Domain tests (28)
│ ├── test_entities.py
│ ├── test_session.py
│ ├── test_repositories.py
│ └── test_sqlite_repos.py
└── README.md

text

---

## Prerequisites

- Python 3.11 or higher
- pip

---

## Installation

```bash
git clone https://github.com/your-username/Two-Bank-ATM-Simple.git
cd Two-Bank-ATM-Simple/twobank_atm_cli

python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows
source .venv/bin/activate        # macOS / Linux

pip install -r requirements.txt
```

---

## Usage

**Graphical interface:**
```bash
python main.py
```

**CLI interface:**
```bash
python -m presentation.cli
```

---

## Tests

```bash
pytest -v          # all tests
pytest --cov       # with coverage
```

**Current result:** `94 passed, 0 failed`

| File | Type | Tests |
|---|---|---|
| `test_gui.py` | Unit | 13 |
| `test_domain.py` | Unit | 28 |
| `test_repositories.py` | Unit | 14 |
| `test_sqlite_repos.py` | Integration | — |
| **Total** | | **94** |

---

## Documentation

- [ARCHITECTURE.md](./ARCHITECTURE.md) — Detailed architecture docs (EN)
- [ARCHITECTURE.es.md](./ARCHITECTURE.es.md) — Arquitectura en español
- [docs/CHANGELOG.md](./docs/CHANGELOG.md)
- [docs/ROADMAP.md](./docs/ROADMAP.md)

---

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.
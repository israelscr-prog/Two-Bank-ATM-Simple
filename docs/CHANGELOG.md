# CHANGELOG — TWO Bank ATM Simple

Todos los cambios relevantes del proyecto documentados en orden cronológico.

---

## [0.3.0] — 2026-04-16 — GUI

### Added
- `presentation/gui/` — Interfaz gráfica con CustomTkinter
- `presentation/gui/app.py` — Ventana principal y navegación entre frames
- `presentation/gui/login_frame.py` — Pantalla de login con contador de intentos
- `presentation/gui/menu_frame.py` — Menú principal con todas las operaciones
- `main.py` — Modo dual: `python main.py` (GUI) / `python main.py --cli` (CLI)
- `requirements.txt` — Añadido `customtkinter==5.2.2`

---

## [0.2.0] — 2026-04-16 — CLI

### Added
- `presentation/cli.py` — Interfaz de línea de comandos completa
- `application/session.py` — ATMSession con todos los use cases:
  - `authenticate()` — Login con tarjeta y PIN
  - `check_balance()` — Consulta de saldo
  - `withdraw()` — Retirada de efectivo
  - `deposit()` — Ingreso de efectivo
  - `change_pin()` — Cambio de PIN
  - `mini_statement()` — Últimos 5 movimientos
  - `logout()` — Cierre de sesión

---

## [0.1.0] — 2026-04-16 — Fundamentos

### Added
- `domain/enums.py` — `AccountStatus`, `TransactionType`, `ATMStatus`
- `domain/exceptions.py` — Jerarquía de excepciones del dominio:
  - `ATMError` (base)
  - `AuthenticationError`, `CardBlockedError`, `AccountBlockedError`
  - `InsufficientFundsError`, `InvalidAmountError`, `InvalidPinError`
  - `SessionError`, `NotFoundError`
- `domain/entities.py` — Entidades: `Account`, `Card`, `Transaction`, `hash_pin()`
- `infrastructure/repositories.py` — Repositorios en memoria:
  - `InMemoryAccountRepo`
  - `InMemoryCardRepo`
  - `InMemoryTransactionRepo`
- `infrastructure/seed.py` — Datos de prueba: Ana García (1234/1111), Luis Pérez (5678/2222)
- `requirements.txt` — `pytest`, `pytest-cov`, `ruff`
- Estructura base de carpetas: `domain/`, `application/`, `infrastructure/`, `presentation/`, `tests/`

---

## [0.4.0] — 2026-04-16 — CI Pipeline

### Added
- `.github/workflows/ci.yml` — GitHub Actions pipeline
  - Python 3.12 en ubuntu-latest
  - `ruff` para calidad de código
  - `pytest` con cobertura de tests

---

## [0.5.0] — 2026-04-16 — SQLite

### Added
- `infrastructure/sqlite/database.py` — Conexión y schema SQLite
- `infrastructure/sqlite/sqlite_account_repo.py` — Persistencia de cuentas
- `infrastructure/sqlite/sqlite_card_repo.py` — Persistencia de tarjetas
- `infrastructure/sqlite/sqlite_transaction_repo.py` — Persistencia de transacciones
- `main.py` — Modo dual: `--memory` / SQLite por defecto
- `data/` añadido a `.gitignore`

---

## [0.6.0] — 2026-04-16 — Tests SQLite

### Added
- `tests/test_sqlite_repos.py` — 13 tests de integración para SQLite
  - `TestSQLiteAccountRepo` — save, get, update balance/status
  - `TestSQLiteCardRepo` — save, get, update pin/blocked, foreign key
  - `TestSQLiteTransactionRepo` — save, get, limit, orden cronológico
- Fix `sqlite_card_repo.py` — `ON CONFLICT(number)` en vez de `ON CONFLICT(id)`

---
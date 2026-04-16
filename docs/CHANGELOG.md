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

# CHANGELOG — Two-Bank-ATM-Simple

## [Unreleased 0.7.0] — 2026-04-17

### Added
- `tests/test_gui.py` — 13 tests unitarios de GUI sin display real
  - `TestLoginFrame`: authenticate, on_success, error, intentos, bloqueo tras 3 fallos, reset
  - `TestMenuFrame`: balance, withdraw, deposit, mini statement, logout, refresh
  - Fakes de CustomTkinter (`FakeCTkFrame`, `FakeCTkEntry`, `FakeCTkTextbox`, etc.)
    para evitar dependencia de Tcl/Tk en entornos sin display

- `tests/test_domain.py` — 28 tests unitarios de entidades y sesión
  - `TestAccountDeposit`: importe válido, cero, negativo, cuenta bloqueada
  - `TestAccountWithdraw`: retirada válida, cero, negativo, saldo insuficiente, exacto, bloqueada
  - `TestCard`: check_pin correcto/incorrecto, change_pin éxito/pin_incorrecto/formato_inválido/corto
  - `TestATMSessionAuthenticate`: éxito, pin incorrecto, tarjeta bloqueada, cuenta bloqueada
  - `TestATMSessionOperations`: balance, withdraw, deposit, logout, mini_statement vacío
  - `TestATMSessionWithoutLogin`: SessionError en todas las operaciones sin sesión activa

- `tests/test_repositories.py` — 14 tests unitarios de repositorios en memoria
  - `TestInMemoryAccountRepo`: save, get_by_id, overwrite, not_found, múltiples cuentas
  - `TestInMemoryCardRepo`: save, get_by_number, overwrite, not_found, múltiples tarjetas
  - `TestInMemoryTransactionRepo`: save, filtrado por cuenta, límite, orden reciente primero,
    lista vacía, múltiples transacciones

### Fixed
- Error `ModuleNotFoundError: No module named 'customtkinter'` — instalado en el venv correcto
  (`twobank_atm_cli\.venv`) en lugar del venv raíz
- Error `_tkinter.TclError: Can't find a usable tk.tcl` — resuelto sustituyendo widgets reales
  de CTk por clases Fake antes del import de los frames
- Error `unittest.mock.InvalidSpecError: Cannot spec a Mock object` — resuelto usando
  instancias `MagicMock()` en lugar de la clase `MagicMock` en los patches

### Tests
- **Total: 55 tests — 55 passed, 0 failed**

---
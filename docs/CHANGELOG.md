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
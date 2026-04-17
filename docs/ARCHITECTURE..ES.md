# Arquitectura — Two-Bank-ATM

> 🌐 [Read in English](./ARCHITECTURE.EN.md)

Este documento describe la arquitectura del proyecto, la responsabilidad de cada capa, cada carpeta y cada archivo.

---

## Visión general

El proyecto sigue una **arquitectura limpia por capas** inspirada en _Clean Architecture_ de Robert C. Martin. Cada capa solo depende de las capas interiores y nunca al revés. La lógica de negocio (dominio) no conoce ni la base de datos ni la interfaz de usuario.

```
┌─────────────────────────────────┐
│         presentation/           │  ← GUI (CustomTkinter) + CLI
│   gui/app  gui/login  gui/menu  │
│            cli.py               │
└────────────────┬────────────────┘
                 │ usa
┌────────────────▼────────────────┐
│          application/           │  ← Casos de uso
│          session.py             │
└────────────────┬────────────────┘
                 │ usa
┌────────────────▼────────────────┐
│            domain/              │  ← Núcleo — sin dependencias externas
│  entities  enums  exceptions    │
└────────────────┬────────────────┘
                 │ implementado por
┌────────────────▼────────────────┐
│        infrastructure/          │  ← Adaptadores de datos
│  repositories  sqlite/  seed    │
└─────────────────────────────────┘
```

**Regla principal:** `domain/` no importa nada de `infrastructure/`, `application/` ni `presentation/`.

---

## Raíz del repositorio

```
Two-Bank-ATM-Simple/
├── .github/workflows/ci.yml     # Pipeline de CI en GitHub Actions
├── docs/
│   ├── CHANGELOG.md             # Historial de cambios
│   └── ROADMAP.md               # Funcionalidades planificadas
├── twobank_atm_cli/             # Paquete principal de la aplicación
├── README.md                    # Descripción general del proyecto
├── ARCHITECTURE.md              # Este archivo
├── LICENSE
└── .gitignore
```

### `.github/workflows/ci.yml`
Pipeline de integración continua que se ejecuta en cada push o pull request. Pasos: instalar dependencias → lint con ruff → ejecutar pytest. Falla el build si hay errores de lint o tests.

---

## `twobank_atm_cli/`

Paquete raíz de la aplicación. Contiene el código fuente, los tests, la base de datos y las dependencias.

### `main.py`
Punto de entrada de la aplicación. Inicializa la base de datos SQLite, carga los datos de seed (`seed.py`) y lanza la interfaz gráfica (`ATMApp`).

### `requirements.txt`
Lista de dependencias del proyecto:
- `customtkinter` — widgets modernos sobre Tkinter
- `pytest`, `pytest-mock`, `pytest-cov` — testing

### `data/twobank.db`
Archivo SQLite con las tablas `accounts`, `cards` y `transactions`. Se crea automáticamente al ejecutar `main.py` si no existe.

---

## `domain/`

Núcleo del sistema. **No depende de ninguna otra capa del proyecto.** Contiene las reglas de negocio puras.

### `entities.py`
Define las tres entidades principales:

- **`Account`** _(dataclass)_
  - Atributos: `id`, `owner`, `balance`, `currency`, `status`, `transactions`
  - `deposit(amount)` — valida que el importe sea positivo y la cuenta no esté bloqueada, luego incrementa el saldo.
  - `withdraw(amount)` — valida importe, estado de cuenta y saldo suficiente, luego decrementa el saldo.

- **`Card`** _(dataclass)_
  - Atributos: `id`, `number`, `pin_hash`, `account_id`, `blocked`
  - `check_pin(raw_pin)` — compara el hash SHA-256 del PIN introducido con el almacenado.
  - `change_pin(old_pin, new_pin)` — verifica el PIN actual y que el nuevo tenga exactamente 4 dígitos numéricos.

- **`Transaction`** _(dataclass)_
  - Atributos: `id`, `account_id`, `type`, `amount`, `currency`, `created_at`
  - `__str__()` — formatea el movimiento como `[dd/mm/yyyy HH:MM]  TIPO  importe EUR`.

- **`hash_pin(raw)`** — función auxiliar que aplica SHA-256 al PIN en texto plano.

### `enums.py`
Tipos enumerados del dominio:
- **`AccountStatus`** — `ACTIVE`, `BLOCKED`
- **`TransactionType`** — `DEPOSIT`, `WITHDRAWAL`

### `exceptions.py`
Jerarquía de excepciones propias que reemplazan los `ValueError` genéricos:

| Excepción | Cuándo se lanza |
|---|---|
| `ATMError` | Base de todas las excepciones del dominio |
| `AuthenticationError` | PIN incorrecto o tarjeta no encontrada |
| `CardBlockedError` | Tarjeta marcada como bloqueada |
| `AccountBlockedError` | Cuenta con estado `BLOCKED` |
| `InsufficientFundsError` | Retirada mayor que el saldo disponible |
| `InvalidAmountError` | Importe negativo o igual a cero |
| `InvalidPinError` | PIN con formato inválido (no 4 dígitos) |
| `SessionError` | Operación ejecutada sin sesión activa |
| `NotFoundError` | Entidad no encontrada en el repositorio |

---

## `application/`

Orquesta los casos de uso. Conecta el dominio con la infraestructura. Recibe los repositorios por inyección de dependencias en el constructor.

### `session.py` — clase `ATMSession`

Gestiona el ciclo completo de una sesión de cajero:

| Método | Descripción |
|---|---|
| `authenticate(card_number, pin)` | Valida tarjeta, PIN y estado de cuenta. Establece `current_card` y `current_account`. |
| `check_balance()` | Devuelve el saldo formateado como `"Saldo disponible: X.XX EUR"`. |
| `withdraw(amount)` | Delega en `Account.withdraw()` y registra la transacción. |
| `deposit(amount)` | Delega en `Account.deposit()` y registra la transacción. |
| `change_pin(old_pin, new_pin)` | Delega en `Card.change_pin()`. |
| `mini_statement()` | Obtiene los últimos 5 movimientos del repositorio y los formatea. |
| `logout()` | Limpia `current_card` y `current_account`. |
| `_require_session()` | Helper privado — lanza `SessionError` si no hay sesión activa. |
| `_record(tx_type, amount)` | Helper privado — crea y persiste una `Transaction`. |

---

## `infrastructure/`

Adaptadores de persistencia. Implementa el acceso a datos sin que el dominio lo sepa.

### `repositories.py`
Repositorios **en memoria** usados para desarrollo rápido y testing unitario:

- **`InMemoryAccountRepo`** — almacena `Account` en un `dict[UUID, Account]`. Métodos: `save()`, `get_by_id()`.
- **`InMemoryCardRepo`** — almacena `Card` en un `dict[str, Card]` indexado por número de tarjeta. Métodos: `save()`, `get_by_number()`.
- **`InMemoryTransactionRepo`** — almacena `Transaction` en una lista. `get_by_account()` filtra por `account_id`, invierte el orden (más reciente primero) y aplica `limit`.

### `seed.py`
Carga datos de prueba en los repositorios al arrancar la aplicación: cuentas de los dos bancos, tarjetas asociadas y saldos iniciales predefinidos.

### `sqlite/database.py`
Gestiona la conexión a `data/twobank.db`. La función `get_connection()` devuelve una conexión SQLite con `row_factory = sqlite3.Row`. Las tablas se crean con `CREATE TABLE IF NOT EXISTS` al inicializar.

### `sqlite/sqlite_account_repo.py` — `SQLiteAccountRepo`
Guarda y recupera `Account` en la tabla `accounts`. Usa `INSERT OR REPLACE INTO` para manejar tanto inserciones como actualizaciones en una sola operación.

### `sqlite/sqlite_card_repo.py` — `SQLiteCardRepo`
Guarda y recupera `Card` en la tabla `cards`. Igual que el anterior, usa `INSERT OR REPLACE INTO`.

### `sqlite/sqlite_transaction_repo.py` — `SQLiteTransactionRepo`
Inserta `Transaction` en la tabla `transactions`. `get_by_account()` ejecuta una query `SELECT ... ORDER BY created_at DESC LIMIT ?` para devolver las más recientes primero.

---

## `presentation/`

Capa de entrada del usuario. Depende de `application/` pero no del dominio directamente.

### `cli.py`
Interfaz de línea de comandos. Solicita número de tarjeta y PIN por terminal y presenta un menú numerado con todas las operaciones disponibles. Captura excepciones del dominio y muestra mensajes de error legibles.

### `gui/app.py` — clase `ATMApp`
Ventana principal de la aplicación. Inicializa los repositorios SQLite y la `ATMSession`. Gestiona la navegación entre pantallas mostrando `LoginFrame` o `MenuFrame` según el estado de la sesión.

### `gui/login_frame.py` — clase `LoginFrame`
Pantalla de autenticación. Contiene campos para número de tarjeta y PIN. Llama a `session.authenticate()` y gestiona:
- Llamada al callback `on_success` si el login es correcto.
- Mostrar mensaje de error si el PIN es incorrecto.
- Bloquear los campos de entrada tras 3 intentos fallidos.
- `reset()` — limpia el formulario y reinicia el contador de intentos.

### `gui/menu_frame.py` — clase `MenuFrame`
Menú principal tras el login. Muestra el nombre del titular y botones para cada operación:
- `_check_balance()`, `_withdraw()`, `_deposit()`, `_change_pin()`, `_mini_statement()`, `_logout()`
- `_ask_amount()` — diálogo interno para solicitar el importe.
- `refresh()` — actualiza la etiqueta de bienvenida con el nombre del titular.

---

## `tests/`

Suite de tests completa — **94 tests, 0 fallos**.

| Archivo | Tipo | Qué cubre |
|---|---|---|
| `test_gui.py` | Unitario | `LoginFrame` y `MenuFrame` usando Fakes de CTk sin display real |
| `test_domain.py` | Unitario | `Account`, `Card`, `ATMSession` y todas las excepciones del dominio |
| `test_entities.py` | Unitario | Entidades del dominio |
| `test_session.py` | Unitario | Casos de uso de `ATMSession` con repos mockeados |
| `test_repositories.py` | Unitario | `InMemoryAccountRepo`, `InMemoryCardRepo`, `InMemoryTransactionRepo` |
| `test_sqlite_repos.py` | Integración | `SQLiteAccountRepo`, `SQLiteCardRepo`, `SQLiteTransactionRepo` con DB SQLite en memoria |

### Estrategia de testing

- **Tests unitarios** — usan `MagicMock` o repositorios en memoria para aislar cada componente.
- **Tests de integración** — usan una base de datos SQLite `:memory:` real creada en cada test mediante el fixture `clean_db` con `monkeypatch`.
- **Tests de GUI** — evitan instanciar ventanas reales de Tkinter usando clases `Fake*` que replican la interfaz de los widgets CTk sin depender de Tcl/Tk.

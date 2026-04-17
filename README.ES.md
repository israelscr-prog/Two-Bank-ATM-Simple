# Two-Bank-ATM

> 🌐 [Read in English](./README_EN.md)

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Tests](https://img.shields.io/badge/tests-94%20passed-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

Simulador de cajero automático para dos bancos, desarrollado en Python con **arquitectura limpia por capas**. Incluye interfaz gráfica (CustomTkinter), interfaz de línea de comandos (CLI), persistencia en SQLite y suite de tests completa con 94 tests.

---

## Índice

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Tests](#tests)
- [Documentación](#documentación)
- [Licencia](#licencia)

---

## Características

- 🔐 Autenticación con tarjeta y PIN (hash SHA-256)
- 💰 Consulta de saldo, retirada e ingreso de efectivo
- 📋 Mini-extracto de los últimos movimientos
- 🔑 Cambio de PIN con validación de formato
- 🔒 Bloqueo automático tras 3 intentos fallidos
- 🖥️ Interfaz gráfica con CustomTkinter (modo oscuro)
- 💻 Interfaz de línea de comandos (CLI)
- 🗄️ Persistencia de datos con SQLite
- ✅ 94 tests unitarios e integración — 0 fallos

---

## Tecnologías

| Herramienta | Versión | Uso |
|---|---|---|
| Python | 3.14 | Lenguaje principal |
| CustomTkinter | 5.x | Interfaz gráfica |
| SQLite | built-in | Persistencia de datos |
| pytest | 8.x | Framework de testing |
| pytest-mock | 3.x | Mocking en tests |
| pytest-cov | 6.x | Cobertura de tests |

---

## Estructura del proyecto

```
Two-Bank-ATM-Simple/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline CI (lint + tests)
├── docs/
│   ├── CHANGELOG.md
│   └── ROADMAP.md
├── twobank_atm_cli/
│   ├── main.py                 # Punto de entrada
│   ├── requirements.txt
│   ├── application/
│   │   └── session.py          # Casos de uso (ATMSession)
│   ├── domain/
│   │   ├── entities.py         # Account, Card, Transaction
│   │   ├── enums.py            # AccountStatus, TransactionType
│   │   └── exceptions.py       # Excepciones del dominio
│   ├── infrastructure/
│   │   ├── repositories.py     # Repositorios en memoria
│   │   ├── seed.py             # Datos iniciales
│   │   └── sqlite/
│   │       ├── database.py
│   │       ├── sqlite_account_repo.py
│   │       ├── sqlite_card_repo.py
│   │       └── sqlite_transaction_repo.py
│   ├── presentation/
│   │   ├── cli.py              # Interfaz CLI
│   │   └── gui/
│   │       ├── app.py          # Ventana principal
│   │       ├── login_frame.py  # Pantalla de login
│   │       └── menu_frame.py   # Menú principal
│   └── tests/
│       ├── test_gui.py         # Tests de GUI (13)
│       ├── test_domain.py      # Tests de dominio (28)
│       ├── test_entities.py
│       ├── test_session.py
│       ├── test_repositories.py # Tests de repos en memoria (14)
│       └── test_sqlite_repos.py # Tests de integración SQLite
└── README.md
```

---

## Requisitos previos

- Python 3.11 o superior
- pip

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/Two-Bank-ATM-Simple.git
cd Two-Bank-ATM-Simple/twobank_atm_cli

# 2. Crear y activar el entorno virtual
python -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución

**Interfaz gráfica:**
```bash
python main.py
```

**Interfaz CLI:**
```bash
python -m presentation.cli
```

---

## Tests

```bash
# Ejecutar todos los tests
pytest -v

# Con cobertura
pytest --cov

# Solo un módulo
pytest tests/test_domain.py -v
```

**Resultado actual:** `94 passed, 0 failed`

| Archivo | Tipo | Tests |
|---|---|---|
| `test_gui.py` | Unitario | 13 |
| `test_domain.py` | Unitario | 28 |
| `test_entities.py` | Unitario | — |
| `test_session.py` | Unitario | — |
| `test_repositories.py` | Unitario | 14 |
| `test_sqlite_repos.py` | Integración | — |
| **Total** | | **94** |

---

## Documentación

- [ARCHITECTURE.md](./ARCHITECTURE.md) — Descripción detallada de la arquitectura, capas y archivos
- [docs/CHANGELOG.md](./docs/CHANGELOG.md) — Historial de cambios
- [docs/ROADMAP.md](./docs/ROADMAP.md) — Próximas funcionalidades

---

## Licencia

Distribuido bajo la licencia MIT. Consulta el archivo [LICENSE](./LICENSE) para más información.

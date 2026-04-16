# infrastructure/sqlite/database.py — TWO Bank ATM
# Conexión a SQLite y creación del schema de tablas.

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "twobank.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # acceso por nombre de columna
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Crea las tablas si no existen."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS accounts (
                id        TEXT PRIMARY KEY,
                owner     TEXT NOT NULL,
                balance   REAL NOT NULL,
                currency  TEXT NOT NULL,
                status    TEXT NOT NULL DEFAULT 'ACTIVE'
            );

            CREATE TABLE IF NOT EXISTS cards (
                id         TEXT PRIMARY KEY,
                number     TEXT UNIQUE NOT NULL,
                pin_hash   TEXT NOT NULL,
                account_id TEXT NOT NULL,
                blocked    INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id         TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                type       TEXT NOT NULL,
                amount     REAL NOT NULL,
                currency   TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );
        """)
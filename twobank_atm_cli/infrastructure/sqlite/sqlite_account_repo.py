# infrastructure/sqlite/sqlite_account_repo.py — TWO Bank ATM
# Repositorio de cuentas con persistencia SQLite.

import uuid

from domain.entities import Account
from domain.enums import AccountStatus
from domain.exceptions import NotFoundError
from infrastructure.sqlite.database import get_connection


class SQLiteAccountRepo:

    def save(self, account: Account) -> None:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO accounts (id, owner, balance, currency, status)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    balance  = excluded.balance,
                    status   = excluded.status
            """, (
                str(account.id),
                account.owner,
                account.balance,
                account.currency,
                account.status.value,
            ))

    def get_by_id(self, account_id: uuid.UUID) -> Account:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM accounts WHERE id = ?",
                (str(account_id),)
            ).fetchone()

        if not row:
            raise NotFoundError(f"Cuenta {account_id} no encontrada.")

        return Account(
            id=uuid.UUID(row["id"]),
            owner=row["owner"],
            balance=row["balance"],
            currency=row["currency"],
            status=AccountStatus(row["status"]),
        )
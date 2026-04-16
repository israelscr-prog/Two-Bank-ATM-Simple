# infrastructure/sqlite/sqlite_transaction_repo.py — TWO Bank ATM
# Repositorio de transacciones con persistencia SQLite.

import uuid
from datetime import datetime 

from domain.entities import Transaction
from domain.enums import TransactionType
from infrastructure.sqlite.database import get_connection


class SQLiteTransactionRepo:

    def save(self, tx: Transaction) -> None:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO transactions (id, account_id, type, amount, currency, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO NOTHING
            """, (
                str(tx.id),
                str(tx.account_id),
                tx.type.value,
                tx.amount,
                tx.currency,
                tx.created_at.isoformat(),
            ))

    def get_by_account(self, account_id: uuid.UUID, limit: int = 5) -> list[Transaction]:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM transactions
                WHERE account_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (str(account_id), limit)).fetchall()

        return [
            Transaction(
                id=uuid.UUID(row["id"]),
                account_id=uuid.UUID(row["account_id"]),
                type=TransactionType(row["type"]),
                amount=row["amount"],
                currency=row["currency"],
                created_at=datetime.fromisoformat(row["created_at"]),
            )
            for row in rows
        ]
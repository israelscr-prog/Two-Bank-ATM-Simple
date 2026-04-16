# infrastructure/sqlite/sqlite_card_repo.py — TWO Bank ATM
# Repositorio de tarjetas con persistencia SQLite.

import uuid

from domain.entities import Card
from domain.exceptions import NotFoundError
from infrastructure.sqlite.database import get_connection


class SQLiteCardRepo:

    def save(self, card: Card) -> None:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO cards (id, number, pin_hash, account_id, blocked)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(number) DO UPDATE SET
                    pin_hash = excluded.pin_hash,
                    blocked  = excluded.blocked
            """, (
                str(card.id),
                card.number,
                card.pin_hash,
                str(card.account_id),
                int(card.blocked),
            ))

    def get_by_number(self, number: str) -> Card:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM cards WHERE number = ?",
                (number,)
            ).fetchone()

        if not row:
            raise NotFoundError(f"Tarjeta {number} no encontrada.")

        return Card(
            id=uuid.UUID(row["id"]),
            number=row["number"],
            pin_hash=row["pin_hash"],
            account_id=uuid.UUID(row["account_id"]),
            blocked=bool(row["blocked"]),
        )
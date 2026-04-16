# infrastructure/seed.py — TWO Bank ATM
# Datos de prueba precargados para desarrollo y testing manual.

import uuid

from domain.entities import Account, Card, hash_pin
from domain.enums import AccountStatus
from infrastructure.repositories import (
    InMemoryAccountRepo,
    InMemoryCardRepo,
)


def seed(account_repo: InMemoryAccountRepo, card_repo: InMemoryCardRepo) -> None:

    # ── Cuentas ──────────────────────────────────────
    acc1_id = uuid.uuid4()
    acc2_id = uuid.uuid4()

    acc1 = Account(
        id=acc1_id,
        owner="Ana García",
        balance=1500.00,
        currency="EUR",
        status=AccountStatus.ACTIVE,
    )
    acc2 = Account(
        id=acc2_id,
        owner="Luis Pérez",
        balance=300.00,
        currency="EUR",
        status=AccountStatus.ACTIVE,
    )

    account_repo.save(acc1)
    account_repo.save(acc2)

    # ── Tarjetas ─────────────────────────────────────
    card1 = Card(
        id=uuid.uuid4(),
        number="1234",
        pin_hash=hash_pin("1111"),
        account_id=acc1_id,
    )
    card2 = Card(
        id=uuid.uuid4(),
        number="5678",
        pin_hash=hash_pin("2222"),
        account_id=acc2_id,
    )

    card_repo.save(card1)
    card_repo.save(card2)

    # ── Resumen en pantalla ───────────────────────────
    print("=" * 40)
    print("   🏧  TWO Bank ATM — Datos de prueba")
    print("=" * 40)
    print(f"  Tarjeta: 1234  |  PIN: 1111  |  {acc1.owner:<15} |  {acc1.balance:.2f} {acc1.currency}")
    print(f"  Tarjeta: 5678  |  PIN: 2222  |  {acc2.owner:<15} |  {acc2.balance:.2f} {acc2.currency}")
    print("=" * 40)
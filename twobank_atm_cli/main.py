# main.py — TWO Bank ATM
# Punto de entrada: --cli / --gui (default) | --memory / --sqlite (default)

import sys

from application.session import ATMSession


def build_session(use_sqlite: bool) -> ATMSession:
    if use_sqlite:
        from infrastructure.sqlite.database import init_db
        from infrastructure.sqlite.sqlite_account_repo import SQLiteAccountRepo
        from infrastructure.sqlite.sqlite_card_repo import SQLiteCardRepo
        from infrastructure.sqlite.sqlite_transaction_repo import SQLiteTransactionRepo

        init_db()
        account_repo = SQLiteAccountRepo()
        card_repo    = SQLiteCardRepo()
        tx_repo      = SQLiteTransactionRepo()

        # Seed solo si la DB está vacía
        _seed_sqlite_if_empty(account_repo, card_repo)

    else:
        from infrastructure.repositories import (
            InMemoryAccountRepo,
            InMemoryCardRepo,
            InMemoryTransactionRepo,
        )
        from infrastructure.seed import seed

        account_repo = InMemoryAccountRepo()
        card_repo    = InMemoryCardRepo()
        tx_repo      = InMemoryTransactionRepo()
        seed(account_repo, card_repo)

    return ATMSession(account_repo, card_repo, tx_repo)


def _seed_sqlite_if_empty(account_repo, card_repo) -> None:
    """Inserta datos de prueba solo si no hay cuentas en la DB."""
    from infrastructure.sqlite.database import get_connection

    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM accounts").fetchone()[0]

    if count > 0:
        return  # ya tiene datos, no insertar de nuevo

    import uuid
    from domain.entities import Account, Card, hash_pin
    from domain.enums import AccountStatus

    acc1_id = uuid.uuid4()
    acc2_id = uuid.uuid4()

    acc1 = Account(id=acc1_id, owner="Ana García",  balance=1500.00, currency="EUR")
    acc2 = Account(id=acc2_id, owner="Luis Pérez",  balance=300.00,  currency="EUR")

    account_repo.save(acc1)
    account_repo.save(acc2)

    card_repo.save(Card(id=uuid.uuid4(), number="1234", pin_hash=hash_pin("1111"), account_id=acc1_id))
    card_repo.save(Card(id=uuid.uuid4(), number="5678", pin_hash=hash_pin("2222"), account_id=acc2_id))

    print("=" * 40)
    print("   🏧  TWO Bank ATM — Datos de prueba")
    print("=" * 40)
    print("  Tarjeta: 1234  |  PIN: 1111  |  Ana García  |  1500.00 EUR")
    print("  Tarjeta: 5678  |  PIN: 2222  |  Luis Pérez  |   300.00 EUR")
    print("=" * 40)


def main():
    args       = sys.argv[1:]
    use_sqlite = "--memory" not in args   # SQLite por defecto
    use_cli    = "--cli" in args

    session = build_session(use_sqlite)

    if use_cli:
        from presentation.cli import login, menu_principal
        while True:
            if login(session):
                menu_principal(session)
            if input("\n¿Nueva sesión? (s/n): ").strip().lower() != "s":
                print("\n  👋 Hasta pronto.\n")
                break
    else:
        from presentation.gui.app import ATMApp
        app = ATMApp(session)
        app.mainloop()


if __name__ == "__main__":
    main()
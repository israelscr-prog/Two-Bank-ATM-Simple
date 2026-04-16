# main.py — TWO Bank ATM
# Punto de entrada del programa.

from infrastructure.repositories import (
    InMemoryAccountRepo,
    InMemoryCardRepo,
    InMemoryTransactionRepo,
)
from infrastructure.seed import seed
from application.session import ATMSession
from presentation.cli import login, menu_principal


def main() -> None:
    # Setup — repositorios y datos de prueba
    account_repo = InMemoryAccountRepo()
    card_repo    = InMemoryCardRepo()
    tx_repo      = InMemoryTransactionRepo()

    seed(account_repo, card_repo)

    session = ATMSession(account_repo, card_repo, tx_repo)

    # Bucle principal del cajero
    while True:
        if login(session):
            menu_principal(session)

        continuar = input("\n¿Nueva sesión? (s/n): ").strip().lower()
        if continuar != "s":
            print("\n  👋 Hasta pronto.\n")
            break


if __name__ == "__main__":
    main()
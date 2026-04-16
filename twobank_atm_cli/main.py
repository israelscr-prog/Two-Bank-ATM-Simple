# main.py — TWO Bank ATM
# Punto de entrada: --cli para terminal, --gui (o sin argumento) para interfaz gráfica.

import sys

from infrastructure.repositories import (
    InMemoryAccountRepo,
    InMemoryCardRepo,
    InMemoryTransactionRepo,
)
from infrastructure.seed import seed
from application.session import ATMSession


def main():
    account_repo = InMemoryAccountRepo()
    card_repo    = InMemoryCardRepo()
    tx_repo      = InMemoryTransactionRepo()

    seed(account_repo, card_repo)
    session = ATMSession(account_repo, card_repo, tx_repo)

    mode = sys.argv[1] if len(sys.argv) > 1 else "--gui"

    if mode == "--cli":
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
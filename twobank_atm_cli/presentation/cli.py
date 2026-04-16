# presentation/cli.py — TWO Bank ATM
# Interfaz de línea de comandos: login y menú principal.

from application.session import ATMSession
from domain.exceptions import ATMError


# ─────────────────────────────────────────
# Login
# ─────────────────────────────────────────

def login(session: ATMSession) -> bool:
    print("\n╔══════════════════════════════════╗")
    print("║    Bienvenido a TWO Bank ATM 🏧   ║")
    print("╚══════════════════════════════════╝")

    intentos = 0
    while intentos < 3:
        card_number = input("\n  Número de tarjeta : ").strip()
        pin         = input("  PIN               : ").strip()

        try:
            session.authenticate(card_number, pin)
            print(f"\n  ✅ Acceso concedido. Bienvenido/a, {session.current_account.owner}!")
            return True
        except ATMError as e:
            intentos += 1
            remaining = 3 - intentos
            print(f"\n  ⚠  {e}")
            if remaining > 0:
                print(f"     Intentos restantes: {remaining}")

    print("\n  ⛔ Demasiados intentos fallidos. Sesión cancelada.")
    return False


# ─────────────────────────────────────────
# Menú principal
# ─────────────────────────────────────────

def menu_principal(session: ATMSession) -> None:
    while True:
        print("\n┌──────────────────────────────┐")
        print("│       TWO Bank ATM 🏧        │")
        print("├──────────────────────────────┤")
        print("│  1.  Consultar saldo         │")
        print("│  2.  Retirar efectivo        │")
        print("│  3.  Ingresar efectivo       │")
        print("│  4.  Cambiar PIN             │")
        print("│  5.  Últimos movimientos     │")
        print("│  0.  Salir                   │")
        print("└──────────────────────────────┘")

        opcion = input("\n  Elige opción: ").strip()

        try:
            if opcion == "1":
                print(f"\n  💰 {session.check_balance()}")

            elif opcion == "2":
                amount = float(input("  Importe a retirar : "))
                print(f"\n  ✅ {session.withdraw(amount)}")

            elif opcion == "3":
                amount = float(input("  Importe a ingresar: "))
                print(f"\n  ✅ {session.deposit(amount)}")

            elif opcion == "4":
                old = input("  PIN actual         : ").strip()
                new = input("  Nuevo PIN (4 dígitos): ").strip()
                print(f"\n  {session.change_pin(old, new)}")

            elif opcion == "5":
                print(f"\n{session.mini_statement()}")

            elif opcion == "0":
                session.logout()
                print("\n  👋 Sesión cerrada. Retire su tarjeta.")
                break

            else:
                print("\n  ⚠  Opción no válida. Elige entre 0 y 5.")

        except ValueError:
            print("\n  ⚠  Introduce un importe numérico válido.")
        except ATMError as e:
            print(f"\n  ⚠  {e}")
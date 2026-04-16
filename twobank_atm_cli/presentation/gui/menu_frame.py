# presentation/gui/menu_frame.py — TWO Bank ATM
# Menú principal: botones de operaciones y área de resultado.

import customtkinter as ctk
from domain.exceptions import ATMError


class MenuFrame(ctk.CTkFrame):

    def __init__(self, parent, session, on_logout):
        super().__init__(parent, corner_radius=0)
        self.session   = session
        self.on_logout = on_logout  # callback → vuelve al login
        self._build()

    def _build(self):
        # ── Cabecera ──────────────────────────────
        self.welcome_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.welcome_label.pack(pady=(40, 4))

        self.balance_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=15),
            text_color="gray",
        )
        self.balance_label.pack(pady=(0, 30))

        # ── Botones de operaciones ─────────────────
        botones = [
            ("💰  Consultar saldo",       self._check_balance),
            ("💵  Retirar efectivo",       self._withdraw),
            ("🏦  Ingresar efectivo",      self._deposit),
            ("🔑  Cambiar PIN",            self._change_pin),
            ("📋  Últimos movimientos",    self._mini_statement),
        ]

        for texto, comando in botones:
            ctk.CTkButton(
                self,
                text=texto,
                width=300,
                height=44,
                anchor="w",
                font=ctk.CTkFont(size=14),
                command=comando,
            ).pack(pady=5, padx=60)

        # ── Área de resultado ─────────────────────
        self.result_box = ctk.CTkTextbox(
            self,
            width=300,
            height=120,
            font=ctk.CTkFont(family="Courier", size=13),
            state="disabled",
        )
        self.result_box.pack(pady=(20, 10), padx=60)

        # ── Botón salir ───────────────────────────
        ctk.CTkButton(
            self,
            text="Salir / Nueva sesión",
            width=300,
            height=40,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90"),
            command=self._logout,
        ).pack(pady=(0, 30), padx=60)

    # ─────────────────────────────────────────────
    # Helper — mostrar resultado
    # ─────────────────────────────────────────────

    def _show(self, text: str, color: str = "white"):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", text)
        self.result_box.configure(state="disabled")

    def _ask_amount(self, prompt: str) -> float | None:
        dialog = ctk.CTkInputDialog(text=prompt, title="TWO Bank ATM")
        value  = dialog.get_input()
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            self._show("⚠  Introduce un importe numérico válido.")
            return None

    # ─────────────────────────────────────────────
    # Use Cases
    # ─────────────────────────────────────────────

    def _check_balance(self):
        try:
            result = self.session.check_balance()
            self._show(f"💰 {result}")
            self.balance_label.configure(text=result)
        except ATMError as e:
            self._show(f"⚠  {e}")

    def _withdraw(self):
        amount = self._ask_amount("Importe a retirar (EUR):")
        if amount is None:
            return
        try:
            result = self.session.withdraw(amount)
            self._show(f"✅ {result}")
            self.balance_label.configure(text=self.session.check_balance())
        except ATMError as e:
            self._show(f"⚠  {e}")

    def _deposit(self):
        amount = self._ask_amount("Importe a ingresar (EUR):")
        if amount is None:
            return
        try:
            result = self.session.deposit(amount)
            self._show(f"✅ {result}")
            self.balance_label.configure(text=self.session.check_balance())
        except ATMError as e:
            self._show(f"⚠  {e}")

    def _change_pin(self):
        old_dialog = ctk.CTkInputDialog(text="PIN actual:", title="Cambiar PIN")
        old_pin    = old_dialog.get_input()
        if old_pin is None:
            return

        new_dialog = ctk.CTkInputDialog(text="Nuevo PIN (4 dígitos):", title="Cambiar PIN")
        new_pin    = new_dialog.get_input()
        if new_pin is None:
            return

        try:
            result = self.session.change_pin(old_pin, new_pin)
            self._show(result)
        except ATMError as e:
            self._show(f"⚠  {e}")

    def _mini_statement(self):
        try:
            result = self.session.mini_statement()
            self._show(result)
        except ATMError as e:
            self._show(f"⚠  {e}")

    def _logout(self):
        self.session.logout()
        self.on_logout()

    # ─────────────────────────────────────────────
    # Actualizar cabecera al entrar
    # ─────────────────────────────────────────────

    def refresh(self):
        name = self.session.current_account.owner
        self.welcome_label.configure(text=f"Bienvenido/a, {name} 👋")
        self.balance_label.configure(
            text=self.session.check_balance()
        )
        self._show("Selecciona una operación.")
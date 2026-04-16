# presentation/gui/login_frame.py — TWO Bank ATM
# Pantalla de login: introducir tarjeta y PIN.

import customtkinter as ctk
from domain.exceptions import ATMError


class LoginFrame(ctk.CTkFrame):

    def __init__(self, parent, session, on_success):
        super().__init__(parent, corner_radius=0)
        self.session    = session
        self.on_success = on_success  # callback → muestra el menú
        self.intentos   = 0

        self._build()

    def _build(self):
        # ── Logo / Título ─────────────────────────
        ctk.CTkLabel(
            self,
            text="🏧 TWO Bank ATM",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(pady=(50, 5))

        ctk.CTkLabel(
            self,
            text="The Worldwide Only Bank",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 40))

        # ── Tarjeta ───────────────────────────────
        ctk.CTkLabel(self, text="Número de tarjeta", anchor="w").pack(
            fill="x", padx=60
        )
        self.card_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ej: 1234",
            width=300,
            height=40,
        )
        self.card_entry.pack(pady=(4, 16), padx=60)

        # ── PIN ───────────────────────────────────
        ctk.CTkLabel(self, text="PIN", anchor="w").pack(fill="x", padx=60)
        self.pin_entry = ctk.CTkEntry(
            self,
            placeholder_text="····",
            show="●",
            width=300,
            height=40,
        )
        self.pin_entry.pack(pady=(4, 24), padx=60)
        self.pin_entry.bind("<Return>", lambda e: self._login())

        # ── Botón entrar ──────────────────────────
        ctk.CTkButton(
            self,
            text="Entrar",
            width=300,
            height=44,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self._login,
        ).pack(padx=60)

        # ── Mensaje de error ──────────────────────
        self.msg_label = ctk.CTkLabel(
            self,
            text="",
            text_color="#FF5555",
            font=ctk.CTkFont(size=13),
        )
        self.msg_label.pack(pady=(16, 0))

    # ─────────────────────────────────────────────
    # Lógica de login
    # ─────────────────────────────────────────────

    def _login(self):
        card_number = self.card_entry.get().strip()
        pin         = self.pin_entry.get().strip()

        try:
            self.session.authenticate(card_number, pin)
            self.msg_label.configure(text="")
            self.on_success()                     # ← va al menú

        except ATMError as e:
            self.intentos += 1
            remaining = 3 - self.intentos
            self.pin_entry.delete(0, "end")       # limpia el PIN

            if remaining <= 0:
                self.msg_label.configure(text="⛔ Demasiados intentos. Sesión cancelada.")
                self.card_entry.configure(state="disabled")
                self.pin_entry.configure(state="disabled")
            else:
                self.msg_label.configure(
                    text=f"⚠  {e}  —  Intentos restantes: {remaining}"
                )

    def reset(self):
        """Limpia el formulario para una nueva sesión."""
        self.intentos = 0
        self.card_entry.configure(state="normal")
        self.pin_entry.configure(state="normal")
        self.card_entry.delete(0, "end")
        self.pin_entry.delete(0, "end")
        self.msg_label.configure(text="")
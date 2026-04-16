# presentation/gui/app.py — TWO Bank ATM
# Ventana principal: gestiona la navegación entre LoginFrame y MenuFrame.

import customtkinter as ctk

from application.session import ATMSession
from presentation.gui.login_frame import LoginFrame
from presentation.gui.menu_frame import MenuFrame


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ATMApp(ctk.CTk):

    def __init__(self, session: ATMSession):
        super().__init__()
        self.session = session

        # ── Ventana ───────────────────────────────
        self.title("TWO Bank ATM")
        self.geometry("480x680")
        self.resizable(False, False)

        # ── Frames ────────────────────────────────
        self.login_frame = LoginFrame(
            parent=self,
            session=self.session,
            on_success=self._show_menu,
        )
        self.menu_frame = MenuFrame(
            parent=self,
            session=self.session,
            on_logout=self._show_login,
        )

        # Arranca en el login
        self._show_login()

    # ─────────────────────────────────────────────
    # Navegación
    # ─────────────────────────────────────────────

    def _show_login(self):
        self.menu_frame.place_forget()
        self.login_frame.reset()
        self.login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _show_menu(self):
        self.login_frame.place_forget()
        self.menu_frame.refresh()
        self.menu_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
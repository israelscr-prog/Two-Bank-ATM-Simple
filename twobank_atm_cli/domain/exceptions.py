# domain/exceptions.py — TWO Bank ATM
# Reemplaza los ValueError genéricos por excepciones propias del dominio.

class ATMError(Exception):
    """Base para todos los errores del dominio ATM."""
    pass


class AuthenticationError(ATMError):
    """PIN incorrecto o tarjeta no encontrada."""
    pass


class CardBlockedError(ATMError):
    """La tarjeta está bloqueada."""
    pass


class AccountBlockedError(ATMError):
    """La cuenta está bloqueada."""
    pass


class InsufficientFundsError(ATMError):
    """Saldo insuficiente para la operación."""
    pass


class InvalidAmountError(ATMError):
    """Importe inválido (negativo o cero)."""
    pass


class InvalidPinError(ATMError):
    """El PIN no cumple el formato requerido (4 dígitos)."""
    pass


class SessionError(ATMError):
    """Operación sin sesión activa."""
    pass


class NotFoundError(ATMError):
    """Entidad no encontrada en el repositorio."""
    pass
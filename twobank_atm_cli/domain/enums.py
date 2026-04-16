# domain/enums.py — TWO Bank ATM
# Todos los enums del dominio en un solo lugar.

from enum import Enum


class AccountStatus(Enum):
    ACTIVE  = "ACTIVE"
    BLOCKED = "BLOCKED"


class TransactionType(Enum):
    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT    = "DEPOSIT"
    TRANSFER   = "TRANSFER"
    BALANCE    = "BALANCE"


class ATMStatus(Enum):
    IDLE         = "IDLE"
    IN_USE       = "IN_USE"
    OUT_OF_CASH  = "OUT_OF_CASH"
    MAINTENANCE  = "MAINTENANCE"
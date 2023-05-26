from enum import Enum

class TransactionType(Enum):
    Check = "check"
    Online = "online"
    Wire = "wire"
    Cash = "cash"
    ACH = 'ACH'
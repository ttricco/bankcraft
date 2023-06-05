from abc import ABC, abstractmethod

class Transaction(ABC):

    @abstractmethod
    def get_tx_type(self):
        pass



class Cheque(Transaction):
    def __init__(self):
        self._tx_type = "cheque"

    def get_tx_type(self):
        return self._tx_type



class Cash(Transaction):
    def __init__(self):
        self._tx_type = "cash"

    def get_tx_type(self):
        return self._tx_type



class ACH(Transaction):
    """
    ACH stands for Automated Clearing House network.
    ACH is used for all kinds of fund transfer TXs,
    including direct deposit of paycheck and monthly 
    debits for routin payments.
    """
    def __init__(self):
        self._tx_type = "ACH"

    def get_tx_type(self):
        return self._tx_type
 
    

class Wire(Transaction):
    def __init__(self):
        self._tx_type = "wire"

    def get_tx_type(self):
        return self._tx_type



class OnlinePayment(Transaction):
    def __init__(self):
        self._tx_type = "online"
    
    def get_tx_type(self):
        return self._tx_type    

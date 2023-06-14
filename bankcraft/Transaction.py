from abc import ABC, abstractmethod
 
class Transaction(ABC):
    def __init__(self, sender_account, recipient_account, amount,
                  date, sender_id):
        self.transaction_id = f"{date}-{sender_id}"
        self.sender_account = sender_account
        self.recipient_account = recipient_account
        self.amount = amount
        self.date_of_transaction = date
   
    
    def do_transaction(self):
        if self.sender_account and self.sender_account.balance >= self.amount:
            self.sender_account.balance -= self.amount
        if self.recipient_account:
            self.recipient_account.balance += self.amount


    def get_sender_id(self):
        return self.sender_account.owner.unique_id
    

    def get_receiver_id(self):
        return self.recipient_account.owner.unique_id
    
    ######################
class Cheque(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        self._tx_type = "cheque"
        super().__init__(sender_account, recipient_account, amount, date, sender_id)

    def get_tx_type(self):
        return self._tx_type



class Cash(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        self._tx_type = "cash"
        super().__init__(sender_account, recipient_account, amount, date, sender_id)

    def get_tx_type(self):
        return self._tx_type



class ACH(Transaction):
    """
    ACH stands for Automated Clearing House network.
    ACH is used for all kinds of fund transfer TXs,
    including direct deposit of paycheck and monthly 
    debits for routin payments.
    """
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        self._tx_type = "ACH"
        super().__init__(sender_account, recipient_account, amount, date, sender_id)

    def get_tx_type(self):
        return self._tx_type
 
    

class Wire(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        self._tx_type = "wire"
        super().__init__(sender_account, recipient_account, amount, date, sender_id)

    def get_tx_type(self):
        return self._tx_type



class OnlinePayment(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        self._tx_type = "online"
        super().__init__(sender_account, recipient_account, amount, date, sender_id)
    
    def get_tx_type(self):
        return self._tx_type   

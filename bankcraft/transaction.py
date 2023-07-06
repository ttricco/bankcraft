from abc import ABC, abstractmethod


class Transaction(ABC):
    def __init__(self, sender_account, recipient_account, amount,
                 date, sender_id):
        self.transaction_id = f"{date}-{sender_id}"
        self.sender_account = sender_account
        self.recipient_account = recipient_account
        self.amount = amount
        self.date_of_transaction = date
        self._tx_type = None

    def do_transaction(self):
        if (self.sender_account is not None) and (self.sender_account.balance >= self.amount):
            self.sender_account.balance -= self.amount
        if self.recipient_account is not None:
            self.recipient_account.balance += self.amount

    def get_tx_type(self):
        return self._tx_type


class Cheque(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        super().__init__(sender_account, recipient_account, amount, date, sender_id)
        self._tx_type = "cheque"


class Cash(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        super().__init__(sender_account, recipient_account, amount, date, sender_id)
        self._tx_type = "cash"


class ACH(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        super().__init__(sender_account, recipient_account, amount, date, sender_id)
        self._tx_type = "ACH"


class Wire(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        super().__init__(sender_account, recipient_account, amount, date, sender_id)
        self._tx_type = "wire"


class OnlinePayment(Transaction):
    def __init__(self, sender_account, recipient_account, amount, date, sender_id):
        super().__init__(sender_account, recipient_account, amount, date, sender_id)
        self._tx_type = "online"

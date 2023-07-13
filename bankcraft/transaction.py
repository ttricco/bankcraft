class Transaction:
    def __init__(self, sender_account, recipient_account, amount,
                 date, sender_id, txn_counter, txn_type):
        self.transaction_id = f"{txn_counter}-{sender_id}"
        self.sender_account = sender_account
        self.recipient_account = recipient_account
        self.amount = amount
        self.date_of_transaction = date
        self._txn_type = txn_type

    def do_transaction(self):
        self.sender_account.balance -= self.amount
        if self.recipient_account is not None:
            self.recipient_account.balance += self.amount

    def txn_type_is_defined(self):
        return str(self._txn_type).lower() in ["cash", "wire", "online", "ach", "cheque"]

    def txn_is_authorized(self):
        return True

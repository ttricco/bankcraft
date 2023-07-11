class Transaction:
    def __init__(self, sender_account, recipient_account, amount,
                 date, sender_id, txn_counter, txn_type):
        self.transaction_id = f"{txn_counter}-{sender_id}"
        self.sender_account = sender_account
        self.recipient_account = recipient_account
        self.amount = amount
        self.date_of_transaction = date
        self._txn_type = txn_type
        self.check_txn_type()

    def do_transaction(self):
        self.check_txn_type()
        if self.sender_account is not None:
            if self.sender_account.balance >= self.amount:
                self.sender_account.balance -= self.amount
                if self.recipient_account is not None:
                    self.recipient_account.balance += self.amount
            else:
                # print("txn_amount is more than account balance!")
                pass

    def check_txn_type(self):
        if str(self._txn_type).lower() not in ["cash", "wire", "online", "ach", "cheque"]:
            raise ValueError("Undefined txn type")

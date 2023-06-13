
class BankAccount:
    def __init__(self, owner, bank, initial_balance):
        self.owner = owner
        self.bank = bank
        self.balance = initial_balance
        self.bank_account_id = f"{owner.unique_id}-{bank.unique_id}"

    
    


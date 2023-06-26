
class BankAccount:
    def __init__(self, person_owner, bank, initial_balance, account_type):
        self.owner = person_owner
        self.bank = bank
        self.balance = initial_balance
        self.account_type = account_type
        self.bank_account_id = f"{person_owner.unique_id}-{bank.unique_id}"

    
    


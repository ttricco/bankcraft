from mesa import Agent
from bankcraft.bank_account import BankAccount


class GeneralAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.bank_accounts = None

    def step(self):
        pass

    def assign_bank_account(self, model, initial_balance):
        account_types = ['chequing', 'saving', 'credit']
        bank_accounts = [[0] * len(account_types)] * len(model.banks)
        for (bank, bank_counter) in zip(model.banks, range(len(model.banks))):
            for (account_type, account_counter) in zip(account_types, range(len(account_types))):
                bank_accounts[bank_counter][account_counter] = BankAccount(self, bank, initial_balance, account_type)

        return bank_accounts

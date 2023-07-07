from mesa import Agent
from bankcraft.bank_account import BankAccount
from uuid import uuid4
import itertools
from bankcraft.transaction import Transaction


class GeneralAgent(Agent):
    def __init__(self, model):
        self.unique_id = str(uuid4().int)[:10]
        super().__init__(self.unique_id, model)
        self.bank_accounts = None
        self.wealth = 0
        self.txn_counter = 0

    def step(self):
        pass

    def assign_bank_account(self, model, initial_balance):
        account_types = ['chequing', 'saving', 'credit']
        bank_accounts = [[0] * len(account_types)] * len(model.banks)
        for (bank, bank_counter) in zip(model.banks, range(len(model.banks))):
            for (account_type, account_counter) in zip(account_types, range(len(account_types))):
                bank_accounts[bank_counter][account_counter] = BankAccount(self, bank, initial_balance, account_type)
        return bank_accounts
    
    def update_wealth(self):
        self.wealth = sum(account.balance for account in itertools.chain.from_iterable(self.bank_accounts))

    def pay(self, amount, receiver, txn_type, motivation=None):
        if type(receiver) == str:
            receiver = self._payerBusiness
        transaction = Transaction(self.bank_accounts[0][0],
                                  receiver.bank_accounts[0][0],
                                  amount,
                                  self.model.schedule.steps,
                                  self.unique_id,
                                  self.txn_counter,
                                  txn_type)
        transaction.do_transaction()
        self.update_records(receiver, amount, txn_type, motivation)
        self.txn_counter += 1
        self.update_wealth()
        receiver.update_wealth()

    def update_records(self, other_agent, amount, transaction_type, motivation=None):
        transaction_data = {
            "sender": self.unique_id,
            "receiver": other_agent.unique_id,
            "amount": amount,
            "time": self.model.schedule.time,
            "transaction_id": f"{str(self.unique_id)}_{str(self.txn_counter)}",
            "transaction_type": transaction_type,
            "motivation": motivation,
        }
        self.model.datacollector.add_table_row("transactions", transaction_data, ignore_missing=True)

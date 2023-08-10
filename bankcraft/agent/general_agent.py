from mesa import Agent
from bankcraft.bank_account import BankAccount
from uuid import uuid4
import itertools
from bankcraft.transaction import Transaction
from bankcraft.config import hunger_rate
import numpy as np


class GeneralAgent(Agent):
    def __init__(self, model):
        # todo "need an easy-to-read short version id"
        self.unique_id = uuid4().int
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

    def pay(self, amount, receiver, txn_type, description):
        if type(receiver) == str:
            receiver = self._payerBusiness
        transaction = Transaction(self,
                                  receiver,
                                  amount,
                                  self.txn_counter,
                                  txn_type)
        if transaction.txn_type_is_defined() and transaction.txn_is_authorized():
            transaction.do_transaction()
            self.update_records(receiver, amount, txn_type, "chequing", description)

    def update_records(self, other_agent, amount, txn_type, senders_account_type, description):
        transaction_data = {
            "sender": self.unique_id,
            "receiver": other_agent.unique_id,
            "amount": amount,
            "step": self.model.schedule.time,
            "date_time": self.model.current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "txn_id": f"{str(self.unique_id)}_{str(self.txn_counter)}",
            "txn_type": txn_type,
            "sender_account_type": senders_account_type,
            "description": description,
        }
        self.model.datacollector.add_table_row("transactions", transaction_data, ignore_missing=True)
        
    def move(self):
        if self._target_location is not None:
            self.move_to(self._target_location)
            self.motivation.update_motivation('hunger', hunger_rate)
            
    def move_to(self, new_position):
        x, y = self.pos
        x_new, y_new = new_position
        x_distance = x_new - x
        y_distance = y_new - y
        if x_distance > 0:
            x += 1
        elif x_distance < 0:
            x -= 1

        if y_distance > 0:
            y += 1
        elif y_distance < 0:
            y -= 1
            
        self.model.grid.move_agent(self, (x, y))
        self.pos = (x, y)
        
    def distance_to(self, other_agent):
        x, y = self.pos
        x_other, y_other = other_agent.pos
        return np.sqrt((x - x_other) ** 2 + (y - y_other) ** 2)

    def get_nearest(self, agent_type):
        closest = float('inf')
        closest_agent = None
        for agent in self.model.get_all_agents_on_grid():
            if isinstance(agent, agent_type):
                distance = self.distance_to(agent)
                if distance < closest:
                    closest = distance
                    closest_agent = agent
        return closest_agent

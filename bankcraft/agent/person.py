import random
import pandas as pd
import numpy as np
from bankcraft.agent.business import Business
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.merchant import Merchant
from bankcraft.transaction import *
from bankcraft.motivation import Motivation
from bankcraft.steps import steps


class Person(GeneralAgent):
    def __init__(self, model,
                 initial_money,
                 spending_prob,
                 spending_amount,
                 salary):
        super().__init__(model)
        self.money = initial_money
        self.spending_prob = spending_prob
        self.spending_amount = spending_amount

        self.salary = salary
        self.employer = None

        self.motivation = Motivation()
        self.txn_motivation = None
        self.txn_motivation_score = 1
        self.bank_accounts = self.assign_bank_account(model, initial_money)

        self.txn_counter = 0
        self.landlord = Business(model, business_type='Landlord')
        self.payerBusiness = Business(model, business_type='test') # a temporary business for recieving scheduled transactions
        self.schedule_txn = pd.DataFrame()

    def update_motivation(self, key, amount):
        value = self.motivation.motivation_dict[key] - amount/1000
        self.motivation.motivation_dict.update({key: value})

    def reset_motivation(self):
        self.motivation = Motivation()

    def set_home(self, home):
        self.home = home

    def set_social_node(self, social_node):
        self.social_node = social_node

    def set_work(self, work):
        self.work = work

    def updateMoney(self):
        self.money = sum(account[0].balance for account in self.bank_accounts)
        
    def set_schedule_txn(self):
        txn_list = [['Type', 'TotalAmount', 'Frequency', 'Probability', 'Receiver'],
                    ['Rent/Mortgage', np.random.normal(3000, 1000), steps.steps['biweekly'], 1, self.landlord],
                    ['Utilities', np.random.normal(loc=200, scale=50), steps.steps['month'], 1, 'Utility Company'],
                    ['Memberships', random.randrange(0, 100), steps.steps['month'], 0.5, 'Business'],
                    ['Subscriptions', random.randrange(0, 100), steps.steps['month'], 0.5, 'Business'],
                    ['Bills', random.randrange(10, 300), steps.steps['month'], 1, 'Business']]
        self.schedule_txn = pd.DataFrame(txn_list[1:], columns=txn_list[0])

    def pay_schedule_txn(self):
        # for all types of transactions if the probability is met, and step is a multiple of frequency, do the transaction
        for index, row in self.schedule_txn.iterrows():
            if self.model.schedule.steps % row['Frequency'] == 0 and random.random() < row['Probability']:
                self.pay(row['TotalAmount'], row['Receiver'])

    def unscheduled_txn(self):
        for key,value in self.motivation.motivation_dict.items():
            if value < 0:
                self.pay(1000, key)
                

        if  random.random() < 0.1:
            weight = self._social_network_weights
            recipient =  random.choices(list(weight.keys()), weights=list(weight.values()), k=1)[0]
            self.adjust_social_network(recipient)
            if random.random() < self.spending_prob:
                self.pay(self.spending_amount, recipient, 'Social')


    def buy(self, motivation):
        # if there is a merchant agent in this location
        if self.model.grid.is_cell_empty(self.pos) == False:
            # get the agent in this location
            agent = self.model.grid.get_cell_list_contents([self.pos])[0]
            # if the agent is a merchant
            if isinstance(agent, Merchant) and self.money >= agent.price:
                self.pay(agent.price, agent, motivation)
                
            
    def pay(self, amount, receiver,motivation=None):
        if type(receiver) == str:
            receiver = self._payerBusiness
        transaction = Cheque(self.bank_accounts[0][0],
                                            receiver.bank_accounts[0][0],
                                            amount, self.model.schedule.steps,
                                            self.txn_counter
                                            )
        self.updateRecords(receiver, amount, transaction.get_tx_type(), motivation)
        transaction.do_transaction()
        self.txn_counter += 1
        self.updateMoney()
        
    



    def set_social_network_weights(self):
        all_agents = self.model.schedule.agents
        weight = {
            agent: self.model.social_grid.edges[
                self.social_node, agent.social_node
            ]['weight']
            if agent != self
            else 0
            for agent in all_agents
            if isinstance(agent, Person)
        }
        self._social_network_weights = weight


    def adjust_social_network(self, other_agent):
        self._social_network_weights[other_agent] += 0.1
        # have weights to be between 0 and 1
        self._social_network_weights[other_agent] = min(
            self._social_network_weights[other_agent], 1
        )



    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def go_home(self):
        self.model.grid.move_agent(self, self.home)

    def go_work(self):
        self.model.grid.move_agent(self, self.work)

    def updateRecords(self, other_agent, amount, transaction_type, motivation = None):
    # Update the transaction records
        transaction_data = {
            "sender": self.unique_id,
            "receiver": other_agent.unique_id,
            "amount": amount,
            "time": self.model.schedule.time,
            "transaction_id": f"{str(self.unique_id)}_{str(self.txn_counter)}",
            "transaction_type": transaction_type,
            "Motivation": motivation,
        }
        self.model.datacollector.add_table_row("transactions", transaction_data)

    def step(self):
        self.move()
        self.pay_schedule_txn()
        self.unscheduled_txn()

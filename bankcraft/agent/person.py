import random

from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.merchant import Merchant
# from bankcraft.bank_account import BankAccount
from bankcraft.motivation import Motivation
from bankcraft.agent import merchant


class Person(GeneralAgent):
    def __init__(self, unique_id, model,
                 initial_money,
                 spending_prob,
                 spending_amount,
                 salary):
        super().__init__(unique_id, model)
        self.money = initial_money
        self.spending_prob = spending_prob
        self.spending_amount = spending_amount

        self.salary = salary
        self.employer = None

        self.motivation = Motivation()
        self._tx_motiv = None
        self._tx_motiv_score = 1
        self.bank_accounts = self.assign_bank_account(model, initial_money)

    def get_agent_id(self):
        return self.unique_id

    def update_motivation(self, key, amount):
        value = self.motivation.motivation_dict[key] - amount / 1000
        self.motivation.motivation_dict.update({key: value})

    def reset_motivation(self):
        self.motivation = Motivation()

    def setHome(self, home):
        self._home = home

    def setSocialNode(self, social_node):
        self.social_node = social_node

    def setWork(self, work):
        self._work = work

    def spend(self, amount, spending_prob, tx_type, motiv_type):
        if self.random.random() > spending_prob:
            if self.money >= amount:
                self.money -= amount
                self._tx_type = tx_type
                self.update_motivation(motiv_type, amount)
                self._tx_motiv = motiv_type
                self._tx_motiv_score = self.motivation.motivation_dict[motiv_type]

    def setSocialNetworkWeights(self):
        all_agents = self.model.schedule.agents
        weight = {}
        for agent in all_agents:
            if agent != self and isinstance(agent, Person):
                weight[agent] = self.model.social_grid.edges[self.social_node, agent.social_node]['weight']
            else:
                weight[agent] = 0
        self._socialNetworkWeights = weight

    def lend_borrow(self, amount):
        weight = self._socialNetworkWeights
        other_agent = random.choices(list(weight.keys()), weights=list(weight.values()), k=1)[0]
        # change the weights of the edges between the agent and the other agents
        self.adjustSocialNetwork(other_agent)
        # borrowing from other person
        if amount > 0:
            if amount < other_agent.money:
                self.money += amount
                other_agent.money -= amount
        # lending to other person
        elif amount < 0:
            if abs(amount) < self.money:
                self.money += amount
                other_agent.money -= amount

        # return self.unique_id, self.money, other_agent.unique_id, other_agent.money

    def adjustSocialNetwork(self, other_agent):
        self._socialNetworkWeights[other_agent] += 0.1
        # have weights to be between 0 and 1
        if self._socialNetworkWeights[other_agent] > 1:
            self._socialNetworkWeights[other_agent] = 1

    def deposit_withdraw(self, amount):
        # deposit the money
        if amount >= 0:
            self.money += amount
        # withdraw the money
        elif abs(amount) < self.money:
            self.money -= amount

    def buy(self):
        # if there is a merchant agent in this location
        if not self.model.grid.is_cell_empty(self.pos):
            # get the agent in this location
            agent = self.model.grid.get_cell_list_contents([self.pos])[0]
            # if the agent is a merchant
            if isinstance(agent, Merchant):
                # if the agent has enough money to buy
                if self.money >= agent.price:
                    self.money -= agent.price
                    agent.money += agent.price

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def goHome(self):
        self.model.grid.move_agent(self, self._home)

    def goWork(self):
        self.model.grid.move_agent(self, self._work)

    def update_txn_records(self, other_agent, amount):
        transaction_data = {
            "sender": self.unique_id,
            "receiver": other_agent.unique_id,
            "amount": amount,
            "time": self.model.schedule.time
        }
        self.model.datacollector.get_table("transactions").append(transaction_data)

    def step(self):
        # if self.model.schedule.steps == 2:
        #     self.goWork()
        # elif self.model.schedule.steps == 4:
        #     self.goHome()

        # if self.model.schedule.steps == 1:
        #     self.receive_salary(self.salary, Cheque().tx_type(), 'consumer_needs')
        # else:
        #     self.spend(self.spending_amount, self.spending_prob, ACH().tx_type(), 'hunger')
        #     self.lend_borrow(-1000)
        #     self.deposit_withdraw(-50)
        #     self.billPayment()
        #     self.buy()
        #     self.move()
        # amount = random.randint(1,100)
        # recipient = random.choice(self.model.schedule.agents)
        # transaction = ACH(self.bank_accounts[0],
        #                   recipient.bank_accounts[0],
        #                   amount, self.model.schedule.steps+1,
        #                   self.unique_id)
        # transaction.do_transaction()
        # self.model.transactions.append(transaction)
        pass
    # # reseting the motivation scores
    # if self.model.schedule.steps == n:
    #     self.reset_motivation()

from mesa import Agent
import random
from . import Transaction
from . import Motivation
from . import BankAccount
import pandas as pd
from uuid import uuid4


steps = {'10min' : 1 , 'hour' : 6 ,'day': 24 * 6,
          'week': 7 * 24 * 6, 'biweek': 14 * 24 * 6, 
          'month': 30 * 24 * 6, 'year': 365 * 24 * 6}

class GeneralAgent(Agent):
    def __init__(self, model):
        self._unique_id = uuid4()
        super().__init__(self._unique_id, model)
        

    def step(self):
        pass


class Person(GeneralAgent):
    def __init__(self, model,
                initial_money,
                spending_prob,
                spending_amount,
                salary):
        super().__init__( model)
        self._spendingProb = spending_prob
        self._spendingAmount = spending_amount
        self._salary = salary
        
        self.motivation = Motivation.Motivation()
        # define multiple bank_accounts for each agent which can be saving, checking, .. in different banks  
        self.bank_accounts = [BankAccount.BankAccount(self, bank, initial_money) for bank in model.banks]
        #money is the sum of all bank accounts
        self.money = sum([account.balance for account in self.bank_accounts])
        self.transaction_counter = 0
        self._landlord =Business(model=self.model,business_type='Landlord')
        self._payerBusiness = Business(model=self.model,business_type='test') # a temporary business for recieving scheduled transactions
        self.setScheduleTransaction()

    def get_agent_id(self):
        return self.unique_id


    def getMotiv(self):
        return self.motivation.mtv_dict
    

    def modify_motiv_dict(self, key, amount):
            """
            1000 is a benchmarch for altering motivation scores 
            """
            value = self.motivation.mtv_dict[key] + amount/1000
            self.motivation.mtv_dict.update({key : value})


    def reset_motiv_dict(self):
            """
            resets all motivation scores
            """
            self.motivation = Motivation.Motivation()


    def setHome(self, home):
        self._home = home

    def setSocialNode(self, social_node):
        self.social_node = social_node


    def setWork(self, work):
        self._work = work

    def updateMoney(self):
        self.money = sum([account.balance for account in self.bank_accounts])

    def setScheduleTransaction(self):
        schedule_transaction = [['Type', 'TotalAmount', 'Frequency', 'Probability', 'Receiver'],
                                        ['Rent/Morgage',random.randrange(1000,10000) , steps['biweek'] , 1, self._landlord],
                                        ['Utilities',random.randrange(60,300) ,steps['biweek'] , 1, 'Utility Company'],
                                        ['Memberships', random.randrange(0,100) ,steps['month'] , 0.5, 'Business'],
                                        ['Subscriptions',random.randrange(0,100)  ,steps['month'] , 0.5, 'Business'],
                                        ['Bills', random.randrange(10,300) ,steps['month'] , 1, 'Business']]
        self._schedule_transaction = pd.DataFrame(schedule_transaction[1:], columns=schedule_transaction[0])
        
        
    
    def payScheduleTransaction(self):
        # for all types of transactions if the probability is met, and step is a multiple of frequency, do the transaction
        for index, row in self._schedule_transaction.iterrows():
            if self.model.schedule.steps % row['Frequency'] == 0 and random.random() < row['Probability']:
                self.pay(row['TotalAmount'], row['Receiver'], row['Type'])

    def unscheduleTransaction(self):
        for motivation in self.motivation.mtv_dict:
            if self.motivation.mtv_dict[motivation] > 200:
                self.buy(motivation)
                self.modify_motiv_dict(motivation, -100)

        if  random.random() < 0.1:
            weight = self._socialNetworkWeights
            receipient =  random.choices(list(weight.keys()), weights=list(weight.values()), k=1)[0]
            self.adjustSocialNetwork(receipient)
            if random.random() < self._spendingProb:
                self.pay(self._spendingAmount, receipient, 'Social')


    def buy(self, motivation):
        # if there is a merchant agent in this location
        if self.model.grid.is_cell_empty(self.pos) == False:
            # get the agent in this location
            agent = self.model.grid.get_cell_list_contents([self.pos])[0]
            # if the agent is a merchant
            if isinstance(agent, Merchant):
                # if the agent has enough money to buy
                if self.money >= agent.price:
                    self.pay(agent.price, agent, motivation)


    def pay(self, amount, receiver,motivation=None):
        if type(receiver) == str:
            receiver = self._payerBusiness
        transaction = Transaction.Cheque(self.bank_accounts[1],
                                            receiver.bank_accounts[1],
                                            amount, self.model.schedule.steps,
                                            self.transaction_counter
                                            )
        self.updateRecords(receiver, amount, transaction.get_tx_type(), motivation)
        transaction.do_transaction()
        self.transaction_counter += 1
        self.updateMoney()

    def setSocialNetworkWeights(self):
        all_agents = self.model.schedule.agents
        weight = {}
        for agent in all_agents:
            if agent != self :
                weight[agent] = self.model.social_grid.edges[self.social_node, agent.social_node]['weight']
            else:
                weight[agent] = 0
        self._socialNetworkWeights = weight

        
    def adjustSocialNetwork(self, other_agent):
        self._socialNetworkWeights[other_agent] += 0.1
        # have weights to be between 0 and 1
        if self._socialNetworkWeights[other_agent] > 1:
            self._socialNetworkWeights[other_agent] = 1

                
        
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        # modify motivation scores
        if self.pos != new_position:

            self.modify_motiv_dict('fatigue', 10)
            self.modify_motiv_dict('hunger', 10)
        else:
            self.modify_motiv_dict('fatigue', 5)
            self.modify_motiv_dict('hunger', 5)

    def goHome(self):
        self.model.grid.move_agent(self, self._home)

    def goWork(self):
        self.model.grid.move_agent(self, self._work)

    def updateRecords(self, other_agent, amount, transaction_type, motivation = None):
    # Update the transaction records
        transaction_data = {
            "sender": self.unique_id,
            "receiver": other_agent.unique_id,
            "amount": amount,
            "time": self.model.schedule.time,
            "transaction_id": str(self.unique_id) + "_" + str(self.transaction_counter),
            "transaction_type": transaction_type,
            "Motivation" : motivation
        }
        self.model.datacollector.add_table_row("transactions", transaction_data)

    def step(self):
        self.move()
        self.payScheduleTransaction()
        self.unscheduleTransaction()

class Merchant(GeneralAgent):
    def __init__(self,  model, 
                 type,
                 price,
                 initial_money):
        super().__init__( model)
        self.money = initial_money
        self._type = type
        self.price = price

    def step(self):
        pass


class Employer(GeneralAgent):
    def __init__(self,  model):
        super().__init__( model)
    
    def step(self):
        pass

class Business(GeneralAgent):
    def __init__(self,  model, business_type):
        super().__init__( model)
        self._employees = []
        self._name = "Business" + str(self._unique_id)
        self._type = business_type
        self.bank_accounts = [BankAccount.BankAccount(self, bank, 0) for bank in model.banks]
        self._meanPrice = random.randrange(10,100)
        self._meanStd = random.randrange(1,10)
    
    def step(self):
        pass


class Bank(GeneralAgent):
    def __init__(self,  model):
        super().__init__(model)
    
    def step(self):
        pass
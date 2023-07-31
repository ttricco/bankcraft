import random
import pandas as pd
import numpy as np
from bankcraft.agent.business import Business
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.merchant import Merchant
from bankcraft.motivation import Motivation
from bankcraft.config import motivation_threshold, hunger_rate, fatigue_rate, social_rate,steps



class Person(GeneralAgent):
    def __init__(self, model,
                 initial_money):
        super().__init__(model)
        self.type = 'person'
        self.monthly_housing_cost = np.random.normal(2000, 650)
        self.housing_cost_frequency = random.choice([steps['biweekly'], steps['month']])
        self.housing_cost_per_pay = self.monthly_housing_cost * self.housing_cost_frequency / steps['month']

        self.monthly_salary = self.monthly_housing_cost / 0.34  # or np.random.normal(5500, 1800)
        self.salary_frequency = random.choice([steps['biweekly'], steps['month']])
        self.salary_per_pay = self.monthly_salary * self.salary_frequency / steps['month']

        self.has_subscription = random.randint(0, 1)
        self.subscription_amount = self.has_subscription * random.randrange(0, 100)
        self.has_membership = random.randint(0, 1)
        self.membership_amount = self.has_membership * random.randrange(0, 100)

        self.employer = None

        self.motivation = Motivation()
        self.txn_motivation = None
        self.txn_motivation_score = 1

        self.bank_accounts = self.assign_bank_account(model, initial_money)

        self.txn_counter = 0
        self.landlord = Business(model, business_type='Landlord')
        # a temporary business for receiving scheduled transactions
        self._payerBusiness = Business(model, business_type='test')
        self.schedule_txn = pd.DataFrame()
        
        self.spending_prob = random.random()
        self.spending_amount = random.randrange(0, 100)

        self._target_location = None

    def set_home(self, home):
        self.home = home

    def set_best_friend(self, best_friend):
        self.best_friend = best_friend
        
    def set_social_node(self, social_node):
        self.social_node = social_node

    def set_target_location(self, motivation):
        if motivation == 'hunger':
            self._target_location = self.get_nearest(Merchant).pos
        elif motivation == 'fatigue':
            self._target_location = self.home
        elif motivation == 'social':
            #self._target_location = self.get_nearest(Person).pos
            self._target_location = self.best_friend.pos
            
    def set_work(self, work):
        self.work = work
        
    def set_schedule_txn(self):
        txn_list = [['schedule_type', 'Amount', 'pay_date', 'Receiver'],
                    ['Rent/Mortgage', self.housing_cost_per_pay, self.housing_cost_frequency, self.landlord],
                    ['Utilities', np.random.normal(loc=200, scale=50), steps['month'], 'Utility Company'],
                    ['Memberships', self.membership_amount, steps['month'], 'Business'],
                    ['Subscriptions', self.subscription_amount, steps['month'], 'Business'],
                    ['Bills', random.randrange(10, 300), steps['month'], 'Business']]
        self.schedule_txn = pd.DataFrame(txn_list[1:], columns=txn_list[0])

    def pay_schedule_txn(self):
        # for all types of txn if the probability is met and step is a multiple of frequency do the txn
        for index, row in self.schedule_txn.iterrows():
            if self.model.schedule.steps % row['Frequency'] == 0:
                self.pay(row['Amount'], row['Receiver'], "ACH", row['schedule_type'])

    def unscheduled_txn(self):                     
        if random.random() < 0.1:
            weight = self._social_network_weights
            recipient = random.choices(list(weight.keys()), weights=list(weight.values()), k=1)[0]
            self.adjust_social_network(recipient)
            if random.random() < self.spending_prob:
                self.pay(self.spending_amount, recipient, 'ACH', 'social')

    def buy(self, motivation):
        # if there is a merchant agent in this location
        if not self.model.grid.is_cell_empty(self.pos):
            # get the agent in this location
            agent = self.model.grid.get_cell_list_contents([self.pos])[0]
            # if the agent is a merchant
            if isinstance(agent, Merchant):
                hunger = self.motivation.get_motivation(motivation)
                if hunger > 100:
                    price = hunger
                else:
                    price = np.random.beta(a=9, b=2, size=1)[0] * (hunger)
                
                self.pay(price, agent,'ACH' ,motivation)
                self.motivation.update_motivation(motivation, -price)     
                              
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
        
    def live(self):
        self.motivation.update_motivation('hunger', hunger_rate)
        self.motivation.update_motivation('fatigue', fatigue_rate)
        self.motivation.update_motivation('social', social_rate)
        
    def socialize(self):
        #if there is a person in this location
        if not self.model.grid.is_cell_empty(self.pos):
            for agent in self.model.grid.get_cell_list_contents([self.pos]):
                if isinstance(agent, Person):
                    self.adjust_social_network(agent)
                    social_amount = np.random.beta(a=9, b=2, size=1)[0] * (self.motivation.get_motivation('social'))
                    self.motivation.update_motivation('social', -social_amount)
                    break       

    def motivation_handler(self):
        critical_motivation = self.motivation.get_critical_motivation()
        if critical_motivation is not None:
            self.set_target_location(critical_motivation)
            if critical_motivation == 'hunger':
                self.buy('hunger')    
            elif critical_motivation == 'fatigue' and self.pos == self.home:
                fatigue_amount = np.random.beta(a=9, b=2, size=1)[0] * (self.motivation.get_motivation('fatigue'))
                self.motivation.update_motivation('fatigue', -fatigue_amount)
                self.motivation.update_motivation('hunger', hunger_rate * -1)
                self.motivation.update_motivation('social', social_rate * -1)
            elif critical_motivation == 'social':
                self.socialize()
            
                
    def step(self):
        self.live()
        self.motivation_handler()
        self.move()
        self.pay_schedule_txn()
        self.unscheduled_txn()
        

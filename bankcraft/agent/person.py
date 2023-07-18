import random
import pandas as pd
import numpy as np
from bankcraft.agent.business import Business
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.merchant import Merchant
from bankcraft.motivation import Motivation
from bankcraft.steps import steps


class Person(GeneralAgent):
    def __init__(self, model,
                 initial_money):
        super().__init__(model)

        self.monthly_housing_cost = np.random.normal(2000, 650)
        self.housing_cost_frequency = random.choice([steps['biweekly'], steps['month']])
        self.housing_cost_per_pay = self.monthly_housing_cost * self.housing_cost_frequency / steps['month']

        self.yearly_income = np.random.normal(66800, 9000)
        self.salary_frequency = random.choice([steps['biweekly'], steps['month']])
        self.num_pays_per_year = steps['year'] // self.salary_frequency
        self.salary_per_pay = self.yearly_income / self.num_pays_per_year

        self.has_subscription = random.randint(0, 1)
        self.subscription_amount = self.has_subscription * random.randrange(0, 100)
        self.has_membership = random.randint(0, 1)
        self.membership_amount = self.has_membership * random.randrange(0, 100)

        self.employer = None

        self.motivation = Motivation()
        self.txn_motivation = None
        self.txn_motivation_score = 1

        self.bank_accounts = self.assign_bank_account(model, initial_money)

        self.landlord = Business(model, business_type='Landlord')
        # a temporary business for receiving scheduled transactions
        self._payerBusiness = Business(model, business_type='test')
        self.schedule_txn = pd.DataFrame()
        
        self.spending_prob = random.random()
        self.spending_amount = random.randrange(0, 100)

        self._target_location = None
        self.txn_counter = 0

    def set_home(self, home):
        self.home = home

    def set_social_node(self, social_node):
        self.social_node = social_node

    def set_work(self, work):
        self.work = work
        
    def set_schedule_txn(self):
        #  include insurance, car lease, loan, tuition (limited time -> keep track of them in a counter)
        #  if the account balance is not enough they must be paid in future including the interest
        txn_list = [['scheduled_expenses', 'Amount', 'pay_date', 'Receiver'],
                    ['Rent/Mortgage', self.housing_cost_per_pay, self.housing_cost_frequency, self.landlord],
                    ['Utilities', np.random.normal(loc=200, scale=50), steps['month'], 'Utility Company'],
                    ['Memberships', self.membership_amount, steps['month'], 'Business'],
                    ['Subscriptions', self.subscription_amount, steps['month'], 'Business'],
                    ['Bills', random.randrange(10, 300), steps['month'], 'Business']]
        self.schedule_txn = pd.DataFrame(txn_list[1:], columns=txn_list[0])

    def pay_schedule_txn(self):
        for index, row in self.schedule_txn.iterrows():
            if self.model.schedule.steps % row['Frequency'] == 0:
                self.pay(amount=row['Amount'],
                         receiver=row['Receiver'],
                         txn_type="ACH",
                         description=row['scheduled_expenses'])

    def unscheduled_txn(self):
        #  work with motivation (affected by time and date and previous txns)
        #  include buying from merchant, car gas, restaurant, medical expenses, recreational activities,
        #  saving, trip and seasonal expenses
        for motivation in self.motivation.motivation_list:
            if self.motivation.get_motivation(motivation) > 20:
                self._target_location = self.get_nearest(Merchant).pos
                print(f'{self.unique_id} is going to {self._target_location}')
                self.buy(motivation)
                
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
            if isinstance(agent, Merchant) and self.wealth >= agent.price:
                self.pay(agent.price, agent, 'online', motivation)
                print(f'{self.unique_id} bought {motivation} from {agent.unique_id}')
                self.motivation.update_motivation(motivation, -15)

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
        if self._target_location is None:
            self.motivation.update_motivation('hunger', 1)

        else:
            self.move_to(self._target_location)
            self.motivation.update_motivation('hunger', 2)

    def move_to(self, new_position):
        print('moving')
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
        for agent in self.model.get_all_agents():
            if isinstance(agent, agent_type):
                distance = self.distance_to(agent)
                if distance < closest:
                    closest = distance
                    closest_agent = agent
        return closest_agent

    def go_home(self):
        self.model.grid.move_agent(self, self.home)

    def go_work(self):
        self.model.grid.move_agent(self, self.work)

    def step(self):
        self.move()
        self.pay_schedule_txn()
        self.unscheduled_txn()

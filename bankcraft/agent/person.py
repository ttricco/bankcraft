import random
import pandas as pd
import numpy as np
from bankcraft.agent.business import Business
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.merchant import Merchant
from bankcraft.motivation import Motivation
from bankcraft.steps import steps
from bankcraft.config import motivation_threshold, hunger_rate, fatigue_rate, social_rate



class Person(GeneralAgent):
    def __init__(self, model,
                 initial_money):
        super().__init__(model)

        self._monthly_housing_cost = np.random.normal(2000, 650)
        self._housing_cost_frequency = random.choice([steps['biweekly'], steps['month']])
        self._housing_cost_per_pay = self._monthly_housing_cost * self._housing_cost_frequency / steps['month']

        self._yearly_income = np.random.normal(66800, 9000)
        self._salary_frequency = random.choice([steps['biweekly'], steps['month']])
        self._num_pays_per_year = steps['year'] // self._salary_frequency
        self.salary_per_pay = self._yearly_income / self._num_pays_per_year

        self._has_subscription = random.randint(0, 1)
        self._subscription_amount = self._has_subscription * random.randrange(0, 100)
        self._has_membership = random.randint(0, 1)
        self._membership_amount = self._has_membership * random.randrange(0, 100)

        self.employer = None

        self.motivation = Motivation()

        self.bank_accounts = self.assign_bank_account(model, initial_money)

        self._landlord = Business(model, business_type='Landlord')
        # a temporary business for receiving scheduled transactions
        self._payerBusiness = Business(model, business_type='test')
        self.schedule_txn = pd.DataFrame()
        
        self.spending_prob = random.random()
        self.spending_amount = random.randrange(0, 100)

        self._target_location = None
#########################
        self._home = None
        self._work = None
        self._social_node = None

    @property
    def home(self):
        if self._home is None:
            return 0, 0
        else:
            return self._home

    @home.setter
    def home(self, value):
        self._home = value

     # def set_home(self, home):
     #     self.home = home

##############################
    @property
    def work(self):
        if self._work is None:
            return 0, 0
        else:
            return self._work

    @work.setter
    def work(self, value):
        self._work = value

    # def set_work(self, work):
    #     self.work = work

#################################
    @property
    def social_node(self):
        if self._social_node is None:
            return 0
        else:
            return self._social_node

    @social_node.setter
    def social_node(self, value):
        self._social_node = value

    # def set_social_node(self, social_node):
        # self.social_node = social_node

#################################
    def set_target_location(self, motivation):
        if motivation == 'hunger':
            self._target_location = self.get_nearest(Merchant).pos
        elif motivation == 'fatigue':
            self._target_location = self.home
        elif motivation == 'social':
            self._target_location = self.get_nearest(Person).pos


        
    def set_schedule_txn(self):
        #  include insurance, car lease, loan, tuition (limited time -> keep track of them in a counter)
        #  if the account balance is not enough they must be paid in future including the interest
        txn_list = [['scheduled_expenses', 'Amount', 'pay_date', 'Receiver'],
                    ['Rent/Mortgage', self._housing_cost_per_pay, self._housing_cost_frequency, self._landlord],
                    ['Utilities', np.random.normal(loc=200, scale=50), steps['month'], 'Utility Company'],
                    ['Memberships', self._membership_amount, steps['month'], 'Business'],
                    ['Subscriptions', self._subscription_amount, steps['month'], 'Business'],
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
            if isinstance(agent, Merchant) and self.wealth >= agent.price:
                self.pay(agent.price, agent,'ACH' ,motivation)
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
        if self._target_location is not None:
            self.move_to(self._target_location)
            self.motivation.update_motivation('hunger', hunger_rate )

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
        for agent in self.model.get_all_agents_on_grid():
            if isinstance(agent, agent_type):
                distance = self.distance_to(agent)
                if distance < closest:
                    closest = distance
                    closest_agent = agent
        return closest_agent

    def live(self):
        self.motivation.update_motivation('hunger', hunger_rate)
        self.motivation.update_motivation('fatigue', fatigue_rate)
        self.motivation.update_motivation('social', social_rate)
    def socialize(self):
        #if there is a person in this location
        if not self.model.grid.is_cell_empty(self.pos):
            agent = self.model.grid.get_cell_list_contents([self.pos])[0]
            # if the agent is a person
            if isinstance(agent, Person):
                self.adjust_social_network(agent)
                self.motivation.update_motivation('social', social_rate * -10)


    def motivation_handler(self):
        critical_motivation = self.motivation.get_critical_motivation()
        if critical_motivation is not None:
            self.set_target_location(critical_motivation)
            if critical_motivation == 'hunger':
                self.buy('hunger')
            elif critical_motivation == 'fatigue' and self.pos == self.home:
                self.motivation.update_motivation('fatigue', fatigue_rate * -10)
            elif critical_motivation == 'social':
                self.socialize()


    def step(self):
        self.live()
        self.motivation_handler()
        self.move()
        self.pay_schedule_txn()
        self.unscheduled_txn()

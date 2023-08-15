import random
import pandas as pd
import numpy as np
from bankcraft.agent.business import Business
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.merchant import Merchant, Food, Clothes
from bankcraft.motivation import Motivation
from bankcraft.config import steps
from bankcraft.config import motivation_threshold, hunger_rate, fatigue_rate, social_rate, consumerism_rate


class Person(GeneralAgent):
    def __init__(self, model,
                 initial_money):
        super().__init__(model)
        self.type = 'person'
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

        self.schedule_txn = pd.DataFrame()

        self.spending_prob = random.random()
        self.spending_amount = random.randrange(0, 100)

        self._target_location = None

        self._home = None
        self._work = None
        self._social_node = None
        self._social_network_weights = None
        self._best_friend = None
        self._set_schedule_txn()

    @property
    def home(self):
        return self._home

    @home.setter
    def home(self, value):
        self._home = value

    @property
    def work(self):
        return self._work

    @work.setter
    def work(self, value):
        self._work = value

    @property
    def social_node(self):
        return self._social_node

    @social_node.setter
    def social_node(self, value):
        self._social_node = value

    @property
    def best_friend(self):
        return self._best_friend

    @best_friend.setter
    def best_friend(self, person):
        self._best_friend = person


    def set_target_location(self, motivation):
        if motivation == 'hunger':
            self._target_location = self.get_nearest(Food).pos
        elif motivation == 'fatigue':
            self._target_location = self.home
        elif motivation == 'social':
            #self._target_location = self.get_nearest(Person).pos
            self._target_location = self.best_friend.pos
        elif motivation == 'work':
            self._target_location = self.work
        elif motivation == 'consumerism':
            self._target_location = self.get_nearest(Clothes).pos


    def _set_schedule_txn(self):
        #  include insurance, car lease, loan, tuition (limited time -> keep track of them in a counter)
        #  if the account balance is not enough they must be paid in future including the interest
        txn_list = [['scheduled_expenses', 'Amount', 'pay_date', 'Receiver'],
                    ['Rent/Mortgage', self._housing_cost_per_pay, self._housing_cost_frequency, self.model.invoicer["rent/mortgage"]],
                    ['Utilities', np.random.normal(loc=200, scale=50), steps['week'], self.model.invoicer["utilities"]],
                    ['Memberships', self._membership_amount, steps['month'], self.model.invoicer["membership"]],
                    ['Subscriptions', self._subscription_amount, steps['month'], self.model.invoicer["subscription"]],
                    ['Providers', random.randrange(10, 300), steps['month'], self.model.invoicer["net_providers"]]
                    ]
        self.schedule_txn = pd.DataFrame(txn_list[1:], columns=txn_list[0])

    def pay_schedule_txn(self):
        for index, row in self.schedule_txn.iterrows():
            if self.model.schedule.steps % row['pay_date'] == 0:
                self.pay(amount=row['Amount'],
                         receiver=row['Receiver'],
                         txn_type='online',
                         description=row['scheduled_expenses'])

    def unscheduled_txn(self):
        if random.random() < 0.1:
            weight = self._social_network_weights
            recipient = random.choices(list(weight.keys()), weights=list(weight.values()), k=1)[0]
            self.adjust_social_network(recipient)
            if random.random() >= self.spending_prob:
                self.pay(amount=self.spending_amount,
                         receiver=recipient,
                         txn_type='ACH',
                         description='social')

    def buy(self, motivation):
        # if there is a merchant agent in this location
        if self.model.grid.is_cell_empty(self.pos):
            return
        agent = self.model.grid.get_cell_list_contents([self.pos])[0]
            # if the agent is a merchant
        price = 0
        if motivation == 'hunger' and isinstance(agent, Food):
            value = self.motivation.get_motivation(motivation)
            price = value if value > 100 else np.random.beta(a=9, b=2, size=1)[0] * (value)
        elif motivation == 'consumerism' and isinstance(agent, Clothes):
            price = self.motivation.get_motivation(motivation)

        self.pay(price, agent, 'ACH', motivation)
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
        if self.pos != self.home:
            self.motivation.update_motivation('hunger', hunger_rate)
            self.motivation.update_motivation('fatigue', fatigue_rate)
            self.motivation.update_motivation('social', social_rate)
            self.motivation.update_motivation('consumerism', consumerism_rate)
        
    def socialize(self):
        if not self.model.grid.is_cell_empty(self.pos):
            for agent in self.model.grid.get_cell_list_contents([self.pos]):
                if isinstance(agent, Person):
                    self.adjust_social_network(agent)
                    social_amount = np.random.beta(a=9, b=2, size=1)[0] * (self.motivation.get_motivation('social'))
                    self.motivation.update_motivation('social', -social_amount)
                    break       

    def motivation_handler(self):
        if self.model.current_time.weekday() < 5 and\
                (9 <= self.model.current_time.hour <= 12 or 13 <= self.model.current_time.hour <= 17):
            self.motivation.update_motivation('work', motivation_threshold)
        else:
            self.motivation.reset_one_motivation('work')
            
        critical_motivation = self.motivation.get_critical_motivation()
        if critical_motivation is not None:
            self.set_target_location(critical_motivation)
            if critical_motivation == 'hunger':
                self.buy('hunger')    
            elif critical_motivation == 'fatigue' and self.pos == self.home:
                self.motivation.update_motivation('fatigue', -2 * fatigue_rate)
            elif critical_motivation == 'social':
                self.socialize()
            elif critical_motivation == 'consumerism':
                self.buy('consumerism')
                           
    def step(self):
        self.live()
        self.motivation_handler()
        self.move()
        self.pay_schedule_txn()
        self.unscheduled_txn()


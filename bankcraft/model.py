from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
import networkx as nx
from bankcraft.agent.merchant import Merchant
from bankcraft.agent.person import Person
from bankcraft.agent.bank import Bank
from bankcraft.agent.employer import Employer
import csv


class Model(Model):
    def __init__(self, num_people=5, num_merchant=2, initial_money=1000,
                 spending_prob=0.5, spending_amount=100,
                 num_employers=2, num_banks=1):
        super().__init__()

        self._num_people = num_people
        self.num_merchant = num_merchant
        self.schedule = RandomActivation(self)
        self.banks = [Bank(self) for _ in range(num_banks)]
        self.num_employers = num_employers
        self.employers = [Employer(self) for _ in range(self.num_employers)]
        # adding a complete graph with equal weights
        self.social_grid = nx.complete_graph(self._num_people)
        for (u, v) in self.social_grid.edges():
            self.social_grid.edges[u, v]['weight'] = 1 / (num_people - 1)

        self.grid = MultiGrid(width=50, height=50, torus=False)
        self._put_people_in_model(initial_money, spending_prob, spending_amount)
        self._put_merchants_in_model()

        self.datacollector = DataCollector(
            agent_reporters={"wealth": lambda a: a.wealth,
                             'location': lambda a: a.pos,
                             'account_balance': lambda a: a.bank_accounts[0][0].balance,
                             'hunger level': lambda a: a.motivation.hunger if isinstance(a, Person) else None,
                             'fatigue level': lambda a: a.motivation.fatigue if isinstance(a, Person) else None,
                             'social level': lambda a: a.motivation.social if isinstance(a, Person) else None,
                             'consumerism level': lambda a: a.motivation.consumer_needs if isinstance(a, Person) else None,
                             },
            tables={"transactions": ["sender", "receiver", "amount", "step", "txn_id", "txn_type", "description"]}

        )

    def _put_people_in_model(self, initial_money, spending_prob, spending_amount):
        for i in range(self._num_people):
            person = Person(self, initial_money)
            if i % 2 == 0:
                self.employers[0].employees.append(person)
                person.employer = self.employers[0]
            elif i % 2 == 1:
                self.employers[1].employees.append(person)
                person.employer = self.employers[1]
            # add agent to grid in random position
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            person.set_home((x, y))
            self.grid.place_agent(person, (x, y))
            # choosing another location as work
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            person.set_work((x, y))
            self.schedule.add(person)
            person.set_social_node(i)
        for i in self.employers:
            self.schedule.add(i)
        # set social network weights
        for person in self.schedule.agents:
            if isinstance(person, Person):
                person.set_social_network_weights()

    def _put_merchants_in_model(self):
        for _ in range(self.num_merchant):
            merchant = Merchant(self, "Restaurant", 10, 1000)
            # choosing location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(merchant, (x, y))
            
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run(self, no_steps):
        for _ in range(no_steps):
            self.step()
        return self.get_agents(), self.get_transactions()

    def get_transactions(self):
        return self.datacollector.get_table_dataframe("transactions")
    
    def get_agents(self):
        return self.datacollector.get_agent_vars_dataframe()


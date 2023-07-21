from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
import networkx as nx
from bankcraft.agent.merchant import Merchant
from bankcraft.agent.person import Person
from bankcraft.agent.bank import Bank
from bankcraft.agent.employer import Employer


class Model(Model):
    def __init__(self, num_people=15, num_merchant=2, initial_money=1000,
                 num_employers=2, num_banks=1):
        super().__init__()

        self._num_people = num_people
        self._num_merchant = num_merchant
        self._num_banks = num_banks
        self.schedule = RandomActivation(self)
        self.banks = [Bank(self) for _ in range(self._num_banks)]
        self._num_employers = num_employers
        self.employers = [Employer(self) for _ in range(self._num_employers)]
        # adding a complete graph with equal weights
        self.social_grid = nx.complete_graph(self._num_people)
        for (u, v) in self.social_grid.edges():
            self.social_grid.edges[u, v]['weight'] = 1 / (self._num_people - 1)

        self.grid = MultiGrid(width=50, height=50, torus=False)
        self._put_people_in_model(initial_money)
        self._put_employers_in_model()
        self._put_banks_in_model()
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
            tables={"transactions": ["sender", "receiver", "amount", "step",
                                     "txn_id", "txn_type", "sender_account_type", "description"]}

        )

    def get_num_people(self):
        return self._num_people

    def get_num_employers(self):
        return self._num_employers

    def get_num_merchants(self):
        return self._num_merchant

    def get_num_banks(self):
        return self._num_banks

    def _put_people_in_model(self, initial_money):
        for i in range(self._num_people):
            person = Person(self, initial_money)
            j = i % self._num_employers
            self.employers[j].add_employee(person)
            person.employer = self.employers[j]

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

        # set social network weights
        for person in self.schedule.agents:
            if isinstance(person, Person):
                person.set_social_network_weights()

    def _put_employers_in_model(self):
        for i in self.employers:
            self.schedule.add(i)

    def _put_banks_in_model(self):
        for i in self.banks:
            self.schedule.add(i)

    def _put_merchants_in_model(self):
        for _ in range(self._num_merchant):
            merchant = Merchant(self, "Restaurant", 10, 1000)
            # choosing location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(merchant, (x, y))
            self.schedule.add(merchant)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run(self, no_steps):
        for _ in range(no_steps):
            self.step()
        return self.get_agents_info(), self.get_txn_info()

    def get_txn_info(self):
        return self.datacollector.get_table_dataframe("transactions")
    
    def get_agents_info(self):
        return self.datacollector.get_agent_vars_dataframe()

    def get_all_agents_on_grid(self):
        all_agents = []
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            all_agents.extend(cell_content)
        return all_agents

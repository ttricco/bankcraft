from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
import networkx as nx
from bankcraft.agent.merchant import Merchant
from bankcraft.agent.person import Person
from bankcraft.agent.bank import Bank
from bankcraft.agent.employer import Employer
import datetime


class Model(Model):
    def __init__(self, num_people=6, num_merchant=2, initial_money=1000,
                 spending_prob=0.5, spending_amount=100,
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

        self.grid = MultiGrid(width=15, height=15, torus=False)
        self._put_employers_in_model()
        self._put_people_in_model(initial_money)
        self._put_merchants_in_model()
        self._set_best_friends()
        self._start_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
        self._one_step_time = datetime.timedelta(minutes=10)
        self.current_time = self._start_time
        self.datacollector = DataCollector(
            agent_reporters={'date_time': lambda a: a.model.current_time.strftime("%Y-%m-%d %H:%M:%S"),
                             'wealth': lambda a: a.wealth,
                             'location': lambda a: a.pos,
                             'Agent type': lambda a: a.type,
                             'account_balance': lambda a: a.bank_accounts[0][0].balance,
                             'hunger level': lambda a: a.motivation.hunger if isinstance(a, Person) else None,
                             'fatigue level': lambda a: a.motivation.fatigue if isinstance(a, Person) else None,
                             'social level': lambda a: a.motivation.social if isinstance(a, Person) else None,
                             'consumerism level': lambda a: a.motivation.consumerism if isinstance(a, Person) else None,
                             },
            tables={"transactions": ["sender", "receiver", "amount", "step", "date_time",
                                     "txn_id", "txn_type", "sender_account_type", "description"]}

        )

    def _place_randomly_on_grid(self, agent):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))
        return x, y

    def _put_employers_in_model(self):
        for employer in self.employers:
            employer.location = self._place_randomly_on_grid(employer )
            self.schedule.add(employer)

    def _put_people_in_model(self, initial_money):
        for i in range(self._num_people):
            person = Person(self, initial_money)
            j = i % self._num_employers
            self.employers[j].add_employee(person)
            person.employer = self.employers[j]
            person.work = person.employer.location
            person.home = self._place_randomly_on_grid(person)
            self.schedule.add(person)
            person.social_node = i

        for person in self.schedule.agents:
            if isinstance(person, Person):
                person.set_social_network_weights()

    def _put_merchants_in_model(self):
        for _ in range(self._num_merchant):
            merchant = Merchant(self, "Restaurant", 10, 1000)
            merchant.location = self._place_randomly_on_grid(merchant)
            self.schedule.add(merchant)

    def _set_best_friends(self):
        person_agents = [agent for agent in self.schedule.agents if isinstance(agent, Person)]
        for i in range(0, len(person_agents), 2):
            person_agents[i].best_friend = person_agents[i+1]
            person_agents[i+1].best_friend = person_agents[i]

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.current_time += self._one_step_time

    def run(self, no_steps):
        for _ in range(no_steps):
            self.step()
        return self

    def get_transactions(self):
        return self.datacollector.get_table_dataframe("transactions")
    
    def get_agents(self):
        return self.datacollector.get_agent_vars_dataframe()

    def get_all_agents_on_grid(self):
        all_agents = []
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            all_agents.extend(cell_content)
        return all_agents

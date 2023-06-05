from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid, MultiGrid
import networkx as nx
from uuid import uuid4
import matplotlib.pyplot as plt
from .agent import Person, Merchant

class Model(Model):
    def __init__(self, num_people=10, num_merchant=2, initial_money=1000,
                 spending_prob=0.5,  spending_amount=100,
                 salary=1000 ):
        super().__init__()

        self._num_people = num_people
        self.num_merchant = num_merchant
        self.schedule = RandomActivation(self)

        # adding a complete graph with equal weights
        self.social_grid = nx.complete_graph(self._num_people)
        for (u, v) in self.social_grid.edges():
            self.social_grid.edges[u, v]['weight'] = 1/(num_people-1)

        # adding grid
        self.grid = MultiGrid(width = 50,height= 50, torus=False)
        
        # Adding PeopleAgents
        for i in range(self._num_people):
            person = Person(uuid4(), self, initial_money, spending_prob, spending_amount, salary)
            # add agent to grid in random position
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            person.setHome((x,y))
            self.grid.place_agent(person, (x, y))
            # choosing another location as work
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            person.setWork((x,y))
            
            self.schedule.add(person)
            person.setSocialNode(i)

        # Adding MerchantAgents
        for i in range(self.num_merchant):
            merchant = Merchant(uuid4(), self, "Restaurant", 10, 1000)
                        # choosing location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            self.grid.place_agent(merchant, (x,y))



        self.datacollector = DataCollector(
             # collect agent money for person agents
             
            agent_reporters = {"Money": lambda a: a.money,
                                'tx_type': lambda a: a.get_tx_type(),
                               'location': lambda a: a.pos},

            # collect model 
            model_reporters = {"social_network_edges": lambda m: m.social_grid.edges(),
                                "social_network_nodes": lambda m: m.social_grid.nodes(),}
                                )
        


    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)



    def run(self, no_steps):
        for i in range(no_steps):
            self.step()

        # collect model state
        self.datacollector.collect(self)
        self.datacollector.get_model_vars_dataframe().to_csv("model_state.csv", mode='a', header=True)
        agent_money = self.datacollector.get_agent_vars_dataframe()

        return (agent_money)
    



 

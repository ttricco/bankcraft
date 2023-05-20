from mesa import Model
from mesa.time import RandomActivation
from agent import Person
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
import networkx as nx

class Model(Model):
    def __init__(self, num_people = 10, INITIAL_MONEY=1000, 
                 SPENDING_PROB = 0.5, SPENDING_AMOUNT = 100,
                 SALARY = 1000):
        
        self.num_people = num_people
        self.schedule = RandomActivation(self)

        # adding a network
        self.G = nx.erdos_renyi_graph(self.num_people, 0.5)
        self.grid = NetworkGrid(self.G)
        
        # Adding PeopleAgents
        for i,node in enumerate(self.G.nodes()):
            person = Person(i, self, INITIAL_MONEY, 
                 SPENDING_PROB, SPENDING_AMOUNT, SALARY)
            self.schedule.add(person)

            # add agent to a random node
            self.grid.place_agent(person, node)

        self.datacollector = DataCollector(
             # collect agent money
            agent_reporters = {"Money": lambda a: a.money}
    
        )


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step() 


    def run(self, steps):
        for i in range(steps):
            self.step()

        agent_money = self.datacollector.get_agent_vars_dataframe()
        return (agent_money)



 

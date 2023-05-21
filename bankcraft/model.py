from mesa import Model
from mesa.time import RandomActivation
from agent import Person
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid
import networkx as nx
import pandas as pd

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
            agent_reporters = {"Money": lambda a: a.money},
            # collect model state
            model_reporters = {'graph': lambda m: m.grid.get_all_cell_contents(), })


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step() 


    def run(self, steps):
        # start model from previous state
        try:
            self.datacollector = DataCollector.from_dataframe(pd.read_csv("model_state.csv"))
        except:
            pass

        for i in range(steps):
            self.step()

        # collect model state
        self.datacollector.collect(self)
        # append model state in the existing file
        self.datacollector.get_model_vars_dataframe().to_csv("model_state.csv", mode='a', header=False)
        agent_money = self.datacollector.get_agent_vars_dataframe()
        return (agent_money)
    



 

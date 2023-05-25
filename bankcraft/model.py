from mesa import Model
from mesa.time import RandomActivation
from agent import Person
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid, MultiGrid
import networkx as nx

class Model(Model):
    def __init__(self, num_people = 10, INITIAL_MONEY=1000, 
                 SPENDING_PROB = 0.5, SPENDING_AMOUNT = 100,
                 SALARY = 1000 ):
        super().__init__()

        self.num_people = num_people
        self.schedule = RandomActivation(self)

        # adding a network
        self.social_grid = nx.erdos_renyi_graph(self.num_people, 0.3)

        # adding grid
        self.grid = MultiGrid(width = 50,height= 50, torus=True)
        
        # Adding PeopleAgents
        for i in range(self.num_people):
            person = Person(i, self, INITIAL_MONEY, SPENDING_PROB, SPENDING_AMOUNT, SALARY)
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


        self.datacollector = DataCollector(
             # collect agent money
            agent_reporters = {"Money": lambda a: a.money,
                               'location': lambda a: a.pos},

            # collect model 
            model_reporters = {"social_network_edges": lambda m: m.social_grid.edges(),
                                "social_network_nodes": lambda m: m.social_grid.nodes(),})
        


    def step(self):
        self.datacollector.collect(self)
        self.schedule.step() 


    def run(self, steps):
        
        for i in range(steps):
            self.step()

        # collect model state
        self.datacollector.collect(self)
        self.datacollector.get_model_vars_dataframe().to_csv("model_state.csv", mode='a', header=True)
        agent_money = self.datacollector.get_agent_vars_dataframe()

        return (agent_money)
    



 

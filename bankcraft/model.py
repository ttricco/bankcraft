from mesa import Model
from mesa.time import RandomActivation, SimultaneousActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid, MultiGrid
import networkx as nx
from .agent import Person, Merchant, Bank

class Model(Model):
    def __init__(self, num_people=5, num_merchant=2, initial_money=1000,
                 spending_prob=0.5,  spending_amount=100,
                 salary=1000 ):
        super().__init__()

        self._num_people = num_people
        # self._num_banks = 1
        self.num_merchant = num_merchant
        self.schedule = RandomActivation(self)
        self.banks = [Bank(self) for i in range(5)]

        # adding a complete graph with equal weights
        self.social_grid = nx.complete_graph(self._num_people)
        for (u, v) in self.social_grid.edges():
            self.social_grid.edges[u, v]['weight'] = 1/(num_people-1)

        # adding grid
        self.grid = MultiGrid(width = 50,height= 50, torus=False)
        
        self.put_agents_in_model(initial_money, spending_prob, spending_amount, salary)

        self.datacollector = DataCollector(
             # collect agent money for person agents
             
            agent_reporters = {"Money": lambda a: a.money,
                                'tx_motiv': lambda a: a.get_tx_motiv(),
                                'tx_motiv_score': lambda a: a.get_tx_motiv_score(),
                               'location': lambda a: a.pos,
                               'account_balance': lambda a: a.bank_accounts[1].balance
                               },


            tables= {"transactions": ["sender", "receiver", "amount", "time", "transaction_id","transaction_type"],
                        "agents": ["id", "money", "location"]}

                                )
    
    def put_agents_in_model(self, initial_money, spending_prob, spending_amount, salary):
        for i in range(self._num_people):
            person = Person( self,
                             initial_money, spending_prob, spending_amount, salary)

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

        # set social network weights
        for person in self.schedule.agents:
            person.setSocialNetworkWeights()

        # Adding MerchantAgents
        for i in range(self.num_merchant):
            merchant = Merchant(self, "Restaurant", 10, 1000)
                        # choosing location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            self.grid.place_agent(merchant, (x,y))

    

    def step(self):

        self.schedule.step()
        self.datacollector.collect(self)



    def run(self, no_steps):
        for i in range(no_steps):
            self.step()

        # collect model state
        self.datacollector.collect(self)

        agents_df = self.datacollector.get_agent_vars_dataframe()
        transactions_df = self.datacollector.get_table_dataframe("transactions")

        return agents_df, transactions_df
    
        


 

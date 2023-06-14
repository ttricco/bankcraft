from mesa import Model
from mesa.time import RandomActivation, SimultaneousActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid, MultiGrid
import networkx as nx
from uuid import uuid4
import matplotlib.pyplot as plt
from .agent import Person, Merchant, Bank, Employer
import csv
import random

class Model(Model):
    def __init__(self, num_people=50, num_merchant=2, initial_money=1000,
                 spending_prob=0.5,  spending_amount=100,
                 salary=1000, num_employers=2 ):
        super().__init__()

        self._num_people = num_people
        self.num_merchant = num_merchant
        self.schedule = RandomActivation(self)
        self.banks = [Bank(i+1, self) for i in range(5)]
        self.transactions = [] 
        self.num_employers = num_employers
        # adding a complete graph with equal weights
        self.social_grid = nx.complete_graph(self._num_people)
        for (u, v) in self.social_grid.edges():
            self.social_grid.edges[u, v]['weight'] = 1/(num_people-1)

        # adding grid
        self.grid = MultiGrid(width = 50,height= 50, torus=False)
        

        # Adding PeopleAgents
        for i in range(self._num_people):
            person = Person(uuid4(), self,
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

        # Adding Employees 
        for i in range(self.num_employers):
            employer = Employer(uuid4(), self)
            employer.employees = random.choices(self.schedule.agents, k=10)
            self.schedule.add(employer)



        # Adding Employees 
        for i in range(self.num_employers):
            employer = Employer(uuid4(), self)
            employer.employees = random.choices(self.schedule.agents, k=10)
            self.schedule.add(employer)



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
                                'tx_motiv': lambda a: a.get_tx_motiv(),
                                'tx_motiv_score': lambda a: a.get_tx_motiv_score(),
                               'location': lambda a: a.pos,
                               'account_balance': lambda a: a.bank_accounts[1].balance
                               },


            tables= {"transactions": ["sender", "receiver", "amount", "time"],
                        "agents": ["id", "money", "location"]}

                                )
        
    

    def step(self):
        # for person in self.schedule.agents:
        #     person.do_transactions()
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
    
        


    def report_transactions(self):
        # Write the transactions to a CSV file.
        with open("transactions.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["TX_id", "Sender_id", "Receiver_id", "Amount","TX_type","Date_of_TX"])
            for transaction in self.transactions:
                writer.writerow([transaction.transaction_id,
                                 transaction.get_sender_id(),
                                 transaction.get_receiver_id(),
                                 transaction.amount,
                                 transaction.get_tx_type(),
                                 transaction.date_of_transaction
                                ])


 

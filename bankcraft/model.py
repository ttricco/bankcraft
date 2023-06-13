from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import NetworkGrid, MultiGrid
import networkx as nx
from uuid import uuid4
import matplotlib.pyplot as plt
from .agent3 import Person, Merchant, Bank
import csv

class Model(Model):
    def __init__(self, num_people=5, num_merchant=2, initial_money=1000,
                 spending_prob=0.5,  spending_amount=100,
                 salary=1000 ):
        super().__init__()

        self._num_people = num_people
        # self._num_banks = 1
        self.num_merchant = num_merchant
        self.schedule = RandomActivation(self)
        self.banks = [Bank(i+1, self) for i in range(5)]
        self.transactions = [] 
        # adding a complete graph with equal weights
        self.social_grid = nx.complete_graph(self._num_people)
        for (u, v) in self.social_grid.edges():
            self.social_grid.edges[u, v]['weight'] = 1/(num_people-1)

        # adding grid
        self.grid = MultiGrid(width = 50,height= 50, torus=False)
        

        # Adding PeopleAgents
        for i in range(self._num_people):
            person = Person(uuid4(), self,
                             initial_money, spending_prob, spending_amount, salary, i, self._num_people)

            # add agent to grid in random position
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            person.setHome((x,y))
            self.grid.place_agent(person, (x, y))
            # choosing another location as work
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            person.setWork((x,y))
                # specify bank accounts to each person
            # for j in ('checking', 'saving'):
                # bank_account = BankAccount( uuid4, person.get_agent_id, bank.get_agent_id, j)
                # person.add_bank_account(bank_account)
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
                                'tx_motiv': lambda a: a.get_tx_motiv(),
                                'tx_motiv_score': lambda a: a.get_tx_motiv_score(),
                               'location': lambda a: a.pos,
                               'account_balance': lambda a: a.bank_accounts[1].balance
                               },

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
        self.report_transactions()
        return (agent_money)
    

    def report_transactions(self):
        # Write the transactions to a CSV file.
        with open("transactions.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Transaction_id", "Sender_id", "Receiver_id", "Amount","Date_of_Transaction"])
            for transaction in self.transactions:
                writer.writerow([transaction.transaction_id,
                                 transaction.get_sender_id(),
                                 transaction.get_receiver_id(),
                                 transaction.amount,
                                 transaction.date_of_transaction
                                ])


 

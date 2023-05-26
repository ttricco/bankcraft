from mesa import Model
from mesa.time import RandomActivation
from agent import Person
from mesa.datacollection import DataCollector


class Model(Model):
    def __init__(self, num_people=10, initial_money=1000, 
                 spending_prob=0.5, spending_amount=100,
                 salary=1000):
        
        self.__num_people = num_people
        self.schedule = RandomActivation(self)
    
        
        # Adding PeopleAgents
        for i in range(self.__num_people):
            person = Person(i, self, initial_money, 
                            spending_prob, spending_amount, salary)
            self.schedule.add(person)

        self.datacollector = DataCollector(
             # collect agent money
            agent_reporters = {"Money": lambda a: a.get_money(),
                               "TX_type": lambda t: t.tx_type,
                               "Motivation": lambda m: m.motivation}
    
        )


    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
         


    def run(self, no_steps):
        for i in range(no_steps):
            self.step()

        agent_money = self.datacollector.get_agent_vars_dataframe()
        return (agent_money)



 

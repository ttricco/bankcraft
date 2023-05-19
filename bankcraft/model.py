from mesa import Model
from mesa.time import RandomActivation
from agent import Person
from mesa.datacollection import DataCollector


class Model(Model):
    def __init__(self, num_people = 10, initial_money=1000, 
                 spending_prob = 0.5, spending_amount = 100,
                 salary = 1000):
        
        self.num_people = num_people
        self.schedule = RandomActivation(self)
    
        
        # Adding PeopleAgents
        for i in range(self.num_people):
            person = Person(i, self, initial_money, 
                 spending_prob, spending_amount, salary)
            self.schedule.add(person)

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



 

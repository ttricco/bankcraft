from mesa import Model
from mesa.time import RandomActivation
from agent import Person
from mesa.datacollection import DataCollector



class Model(Model):
    def __init__(self, NUM_PEOPLE, INITIAL_MONEY, 
                 SPENDING_PROB, SPENDING_AMOUNT, SALARY):
        
        self.num_people = NUM_PEOPLE
        self.schedule = RandomActivation(self)
    
        
        # Adding PeopleAgents
        for i in range(self.num_people):
            person = Person(i, self, INITIAL_MONEY, 
                 SPENDING_PROB, SPENDING_AMOUNT, SALARY)
            self.schedule.add(person)

        self.datacollector = DataCollector(
             # collect agent money
            agent_reporters = {"Money": lambda a: a.money}
    
        )
        
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

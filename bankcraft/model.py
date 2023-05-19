from mesa import Model
from mesa.time import RandomActivation
from agent import Person
from mesa.datacollection import DataCollector



class Model(Model):
    def __init__(self, NUM_PEOPLE = 10, INITIAL_MONEY=1000, 
                 SPENDING_PROB = 0.5, SPENDING_AMOUNT = 100,
                 SALARY = 1000):
        
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


    def run(self, steps):
        for i in range(steps):
            self.step()

        agent_money = self.datacollector.get_agent_vars_dataframe()
        print(agent_money.xs(9, level="Step")["Money"])



 

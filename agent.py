# from abc import ABC, abstractmethod
from mesa import Agent
import random



class GeneralAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Person(GeneralAgent):
    def __init__(self, unique_id, model,
                INITIAL_MONEY,
                SPENDING_PROB,
                SPENDING_AMOUNT):
        super().__init__(unique_id, model)
        self.money = INITIAL_MONEY
        self.__spendingProb = SPENDING_PROB
        self.__spendingAmount = SPENDING_AMOUNT

    def spend(self):
        if self.random.random() > self.__spendingProb:
            if self.money >= self.__spendingAmount:
                self.money -= self.__spendingAmount


    def step(self):
        self.spend()



class Bank(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass



class Merchant(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass



class Employer(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass




class Biller(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass



class Government(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass



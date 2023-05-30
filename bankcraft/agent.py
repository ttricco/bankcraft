from mesa import Agent
import random
import Transaction
from MotivationTypes import Motivation



class GeneralAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class Person(GeneralAgent):
    def __init__(self, unique_id, model,
                initial_money,
                spending_prob,
                spending_amount,
                salary):
        super().__init__(unique_id, model)
        self.__money = initial_money
        self.__spending_prob = spending_prob
        self.__spending_amount = spending_amount
        self.__salary = salary
        self.motivation = None
        self.tx_type = None


    def get_money(self):
        return self.__money


    def spend(self, amount, spending_prob, 
              tx_type, motivation):
        if self.random.random() > spending_prob:
            if self.__money >= amount:
                self.__money -= amount
                self.tx_type = tx_type
                self.motivation = motivation.value
                


    def lend_borrow(self, amount):
        # a random counterparty
        other_agent = self.random.choice(self.model.schedule.agents)
        # borrowing from other person
        if amount > 0:
            if amount < other_agent.__money:
                self.__money += amount
                other_agent.__money -= amount
        # lending to other person
        elif amount < 0: 
            if abs(amount) < self.__money :
                self.__money += amount
                other_agent.__money -= amount
        
        # return self.unique_id, self.money, other_agent.unique_id, other_agent.money


    def deposit_withdraw(self, amount):
        # deposit the money
        if amount >= 0:
            self.money += amount
        # withdraw the money
        elif abs(amount) < self.money:
                self.money -= amount


    def receive_salary(self, salary, 
                       tx_type, motivation):
        if self.model.schedule.steps == 2:
            self.__money += salary
            self.tx_type = tx_type
            self.motivation = motivation.value


    def billPayment(self):
        pass


    def step(self):
        self.receive_salary(self.__salary, 
                            Transaction.Cheque().get_tx_type(), Motivation.ConsumerNeeds)
        self.spend(self.__spending_amount, self.__spending_prob,
                   Transaction.ACH().get_tx_type(), Motivation.Hunger)

        # self.billPayment()




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



class GovernmentBenefit(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass



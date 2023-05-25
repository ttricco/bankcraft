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
                SPENDING_AMOUNT,
                SALARY):
        super().__init__(unique_id, model)
        self.money = INITIAL_MONEY
        self.__spendingProb = SPENDING_PROB
        self.__spendingAmount = SPENDING_AMOUNT
        self.__salary = SALARY


    def setHome(self, home):
        self.__home = home

    def setSocialNode(self, social_node):
        self.social_node = social_node

    def setWork(self, work):
        self.__work = work

    def spend(self):
        if self.random.random() > self.__spendingProb:
            if self.money >= self.__spendingAmount:
                self.money -= self.__spendingAmount

    def setSocialNetwork(self):
        # social_network is a all the nodes that are connected to the agent in the social network
        network = self.model.social_grid
        self.__social_network = list(network.neighbors(self.social_node))

    def lend_borrow(self, amount):
        all_agents = self.model.schedule.agents
        weight = {}
        self.setSocialNetwork()
        for agent in all_agents:
            if agent.social_node  in self.__social_network:
                weight[agent] = 2
            else:
                weight[agent] = 1


        other_agent = random.choices(list(weight.keys()), weights=list(weight.values()), k=1)[0]
    
        # borrowing from other person
        if amount > 0:
            if amount < other_agent.money:
                self.money += amount
                other_agent.money -= amount
        # lending to other person
        elif amount < 0: 
            if abs(amount) < self.money :
                self.money += amount
                other_agent.money -= amount
        
        # return self.unique_id, self.money, other_agent.unique_id, other_agent.money


    def deposit_withdraw(self, amount):
        # deposit the money
        if amount >= 0:
            self.money += amount
        # withdraw the money
        elif abs(amount) < self.money:
                self.money -= amount


    def salary(self):
        if self.model.schedule.step == 2:
            self.money += self.__salary


    def billPayment(self):
        pass

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def goHome(self):
        self.model.grid.move_agent(self, self.__home)

    def goWork(self):
        self.model.grid.move_agent(self, self.__work)


    def step(self):
        if self.model.schedule.step == 2:
            self.goWork()
        elif self.model.schedule.step == 4:
            self.goHome()
        self.spend()
        self.lend_borrow(-1000)
        self.deposit_withdraw(-50)
        self.salary()
        self.billPayment()
        self.move()




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



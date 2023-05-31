from mesa import Agent
import random



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
        self.money = initial_money
        self.__spendingProb = spending_prob
        self.__spendingAmount = spending_amount
        self.__salary = salary


    # def get_money(self):
    #     return self.money

    def setHome(self, home):
        self.__home = home

    def setSocialNode(self, social_node):
        self.social_node = social_node

    def setWork(self, work):
        self.__work = work

    def spend(self, amount, spending_prob):
        if self.random.random() > spending_prob:
            if self.money >= amount:
                self.money -= amount

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


    def receive_salary(self, salary):
        if self.model.schedule.steps == 2:
            self.money += salary



    def billPayment(self):
        pass

    def buy(self):
        # if there is a merchant agent in this location
        if self.model.grid.is_cell_empty(self.pos) == False:
            # get the agent in this location
            agent = self.model.grid.get_cell_list_contents([self.pos])[0]
            # if the agent is a merchant
            if isinstance(agent, Merchant):
                # if the agent has enough money to buy
                if self.money >= agent.price:
                    self.money -= agent.price 
                    agent.money += agent.price                   
        

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
        if self.model.schedule.steps == 2:
            self.goWork()
        elif self.model.schedule.steps == 4:
            self.goHome()

        self.spend(self.__spendingAmount, self.__spendingProb)
        self.lend_borrow(-1000)
        self.deposit_withdraw(-50)
        self.receive_salary(self.__salary)
        self.billPayment()
        self.buy()
        self.move()




class Bank(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass



class Merchant(GeneralAgent):
    def __init__(self, unique_id, model, 
                 type,
                 price,
                 initial_money):
        super().__init__(unique_id, model)
        self.money = initial_money
        self.__type = type
        self.price = price

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



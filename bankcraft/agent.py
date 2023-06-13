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
        self._spendingProb = spending_prob
        self._spendingAmount = spending_amount
        self._salary = salary


    # def get_money(self):
    #     return self.money

    def setHome(self, home):
        self._home = home

    def setSocialNode(self, social_node):
        self.social_node = social_node


    def setWork(self, work):
        self._work = work

    def spend(self, amount, spending_prob):
        if self.random.random() > spending_prob:
            if self.money >= amount:
                self.money -= amount

    def setSocialNetworkWeights(self):
        all_agents = self.model.schedule.agents
        weight = {}
        for agent in all_agents:
            if agent != self :
                weight[agent] = self.model.social_grid.edges[self.social_node, agent.social_node]['weight']
            else:
                weight[agent] = 0
        self._socialNetworkWeights = weight



    def lend_borrow(self, amount):
        weight = self._socialNetworkWeights
        other_agent =  random.choices(list(weight.keys()), weights=list(weight.values()), k=1)[0]
        #change the weights of the edges between the agent and the other agents
        self.adjustSocialNetwork(other_agent)
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

    
    def adjustSocialNetwork(self, other_agent):
        self._socialNetworkWeights[other_agent] += 0.1
        # have weights to be between 0 and 1
        if self._socialNetworkWeights[other_agent] > 1:
            self._socialNetworkWeights[other_agent] = 1


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
        self.model.grid.move_agent(self, self._home)

    def goWork(self):
        self.model.grid.move_agent(self, self._work)

    def updateRecords(self, other_agent, amount):
        # Update the transaction records
            transaction_data = {
                "sender": self.unique_id,
                "receiver": other_agent.unique_id,
                "amount": amount,
                "time": self.model.schedule.time
            }
            self.model.datacollector.get_table("transactions").append(transaction_data)

    def step(self):
        if self.model.schedule.steps == 2:
            self.goWork()
        elif self.model.schedule.steps == 4:
            self.goHome()

        self.spend(self._spendingAmount, self._spendingProb)
        self.lend_borrow(-1000)
        self.deposit_withdraw(-50)
        self.receive_salary(self._salary)
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
        self._type = type
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



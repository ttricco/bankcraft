from mesa import Agent
import random
from . import Transaction
from . import Motivation
from . import BankAccount

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
                salary, person_count, num_people):
        super().__init__(unique_id, model)
        self.money = initial_money
        self._spendingProb = spending_prob
        self._spendingAmount = spending_amount
        self._salary = salary
        self._tx_type = None
        self.motivation = Motivation.Motivation()
        self._tx_motiv = None
        self._tx_motiv_score = 1
        self.bank_accounts = [BankAccount.BankAccount(self, bank, initial_money) for bank in model.banks]
        self.transaction_counter = person_count * num_people

    def get_agent_id(self):
        return self.unique_id


    def get_tx_type(self):
        return self._tx_type


    def get_tx_motiv(self):
        return self._tx_motiv 


    def get_tx_motiv_score(self):
        return self._tx_motiv_score 
    

    def modify_motiv_dict(self, key, amount):
            """
            1000 is a benchmarch for altering motivation scores 
            """
            value = self.motivation.mtv_dict[key] - amount/1000
            self.motivation.mtv_dict.update({key : value})


    def reset_motiv_dict(self):
            """
            resets all motivation scores
            """
            self.motivation = Motivation.Motivation()


    def setHome(self, home):
        self._home = home

    def setSocialNode(self, social_node):
        self.social_node = social_node

    def setWork(self, work):
        self._work = work

    def spend(self, amount, spending_prob, tx_type, motiv_type):
        if self.random.random() > spending_prob:
            if self.money >= amount:
                self.money -= amount
                self._tx_type = tx_type
                self.modify_motiv_dict(motiv_type, amount)
                self._tx_motiv = motiv_type
                self._tx_motiv_score = self.motivation.mtv_dict[motiv_type]
                

    def setSocialNetwork(self):
        # social_network is a all the nodes that are connected to the social_node
        network = self.model.social_grid
        self._social_network = list(network.neighbors(self.social_node))


    def lend_borrow(self, amount):
        all_agents = self.model.schedule.agents
        weight = {}
        self.setSocialNetwork()
        # get the weight of the edges between the agent and the other agents
        # weight is the probability of choosing the other agent
        # weight = {agent: weight of edge between agent and other agent} 
        for agent in all_agents:
            if agent != self :
                weight[agent] = self.model.social_grid.edges[self.social_node, agent.social_node]['weight']
            else:
                weight[agent] = 0

        other_agent = random.choices(list(weight.keys()), weights=list(weight.values()), k=1)[0]
        #change the weights of the edges between the agent and the other agents
        weight[other_agent] += 0.1
        # normalize the weights of self.edges
        for agent in all_agents:
            if agent != other_agent and agent != self:
                self.model.social_grid.edges[self.social_node, agent.social_node]['weight'] /= sum(weight.values())
            elif agent == other_agent:
                self.model.social_grid.edges[self.social_node, agent.social_node]['weight'] = weight[agent]/sum(weight.values())
        
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


    def receive_salary(self, salary, tx_type, motiv_type):
        self.money += salary
        self._tx_type = tx_type
        # receiving salary increases the consumer_needs' score 
        self.modify_motiv_dict(motiv_type, -1 * salary)
        self._tx_motiv = motiv_type
        self._tx_motiv_score = self.motivation.mtv_dict[motiv_type]



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


    def step(self):
        # if self.model.schedule.steps == 2:
        #     self.goWork()
        # elif self.model.schedule.steps == 4:
        #     self.goHome()

        # if self.model.schedule.steps == 1:
        #     self.receive_salary(self._salary, Transaction.Cheque().get_tx_type(), 'consumer_needs')
        # else:
        #     self.spend(self._spendingAmount, self._spendingProb, Transaction.ACH().get_tx_type(), 'hunger')
        #     self.lend_borrow(-1000)
        #     self.deposit_withdraw(-50)
        #     self.billPayment()
        #     self.buy()
        #     self.move()
        amount = random.randint(1,100)
        recipient = random.choice(self.model.schedule.agents)
        transaction = Transaction.ACH(self.bank_accounts[1],
                                              recipient.bank_accounts[1],
                                              amount, self.model.schedule.steps,
                                              self.unique_id)
        transaction.do_transaction()
        self.model.transactions.append(transaction)
        self.transaction_counter += 1

        # # reseting the motivation scors
        # if self.model.schedule.steps == n:
        #     self.reset_motiv_dict()




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




# class Biller(GeneralAgent):
#     def __init__(self, unique_id, model):
#         super().__init__(unique_id, model)
    
#     def step(self):
#         pass



# class GovernmentBenefit(GeneralAgent):
#     def __init__(self, unique_id, model):
#         super().__init__(unique_id, model)
    
#     def step(self):
#         pass

class Bank(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        pass
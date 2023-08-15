from bankcraft.agent.general_agent import GeneralAgent


class Merchant(GeneralAgent):
    def __init__(self, model,
                 type,
                 price,
                 initial_money):
        super().__init__(model)
        self.wealth = initial_money
        self._type = type
        self.price = price
        self.bank_accounts = self.assign_bank_account(model, self.wealth)
        self.type = 'merchant'
        self._location = None

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value
        
class Food(Merchant):
    def __init__(self, model,
                 type,
                 price,
                 initial_money):
        super().__init__(model, type, price, initial_money)
        self.type = 'food'
        self._location = None

class Clothes(Merchant):
    def __init__(self, model,
                 type,
                 price,
                 initial_money):
        super().__init__(model, type, price, initial_money)
        self.type = 'clothes'
        self._location = None


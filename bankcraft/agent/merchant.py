from bankcraft.agent.general_agent import GeneralAgent


class Merchant(GeneralAgent):
    def __init__(self, model,
                 price,
                 initial_money):
        super().__init__(model)
        self.wealth = initial_money
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
                 price,
                 initial_money):
        super().__init__(model, price, initial_money)
        self._location = None

class Clothes(Merchant):
    def __init__(self, model,
                 price,
                 initial_money):
        super().__init__(model, price, initial_money)
        self._location = None


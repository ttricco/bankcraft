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


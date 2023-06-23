from bankcraft.agent.general_agent import GeneralAgent


class Merchant(GeneralAgent):
    def __init__(self, unique_id, model,
                 type,
                 price,
                 initial_money):
        super().__init__(unique_id, model)
        self.money = initial_money
        self._type = type
        self.price = price

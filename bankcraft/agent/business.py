from bankcraft.agent.general_agent import GeneralAgent


class Business(GeneralAgent):
    def __init__(self, model, business_type):
        super().__init__(model)
        self._employees = []
        self._name = "Business" + str(self.unique_id)
        self._type = business_type
        self.initial_money = 0
        self.bank_accounts = self.assign_bank_account(model, self.initial_money)
        self.type = 'business'


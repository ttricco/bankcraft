from bankcraft.agent.general_agent import GeneralAgent


# include landlord (rent and mortgage), utility companies (hydro, natural gas),
# Internet service providers (Internet, phones, cable), gym, club, Insurance companies,
class Business(GeneralAgent):
    def __init__(self, model, business_type):
        super().__init__(model)
        self._employees = []
        self._name = "Business" + str(self.unique_id)
        self._type = business_type
        self.initial_money = 0
        self.bank_accounts = self.assign_bank_account(model, self.initial_money)


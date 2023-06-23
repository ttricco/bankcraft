from bankcraft.agent.general_agent import GeneralAgent


class Bank(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

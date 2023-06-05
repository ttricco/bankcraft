class Bank:
    def __init__(self):
        self.banks = {}

    def add_bank(self, bank_name):
        self.banks[bank_name] = {}

    def add_agent(self, agent_id, bank_name):
        self.banks[bank_name][agent_id] = {
            'saving': 0, 
            'checking': 0
        }

    def get_agent_balance(self, agent_id, bank_name):
        return self.banks[bank_name][agent_id]
    
    def update_balance(self, agent_id, bank_name, account_type, amount):
        self.banks[bank_name][agent_id][account_type] += amount

        
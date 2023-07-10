class Motivation:
    def __init__(self):
        self.hunger = 1
        self.fatigue = 1
        self.social = 1
        self.consumer_needs = 1
        self.motivation_list = ['hunger', 'fatigue', 'social', 'consumer_needs']

    def update_motivation(self, key, amount):
        if hasattr(self, key):
            setattr(self, key, getattr(self, key) + amount)
        else:
            return "Invalid key"

    def reset_motivation(self):
        self.hunger = 1
        self.fatigue = 1
        self.social = 1
        self.consumer_needs = 1
        
    def get_motivation(self, key):
        return getattr(self, key) if hasattr(self, key) else "Invalid key"
        

    

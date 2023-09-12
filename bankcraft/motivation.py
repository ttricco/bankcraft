from bankcraft.config import motivation_threshold


class Motivation:
    def __init__(self):
        self.hunger = 1
        self.fatigue = 1
        self.social = 1
        self.consumerism = 1
        self.work = 1
        self.motivation_list = ['hunger', 'fatigue', 'social', 'consumerism', 'work']

    def update_motivation(self, key, amount):
        if hasattr(self, key):
            if getattr(self, key) + amount > 0:
                setattr(self, key, getattr(self, key) + amount)
            else:
                setattr(self, key, 0)
        else:
            return "Invalid key"

    def reset_motivation(self):
        self.hunger = 1
        self.fatigue = 1
        self.social = 1
        self.consumerism = 1
        self.work = 1
        
    def get_motivation(self, key):
        return getattr(self, key) if hasattr(self, key) else "Invalid key"

    def get_critical_motivation(self):
        # find maximum motivation if above threshold
        max_motivation, max_motivation_value = self.get_max_motivation()
        if max_motivation_value > motivation_threshold:
            return max_motivation
    
    def get_max_motivation(self):
        max_motivation_value = 0
        max_motivation = None
        for motivation in self.motivation_list:
            if self.get_motivation(motivation) > max_motivation_value:
                max_motivation = motivation
                max_motivation_value = self.get_motivation(motivation)
        return max_motivation, max_motivation_value
    
    def reset_one_motivation(self, motivation):
        setattr(self, motivation, 1)

from bankcraft.config import steps

class Clock:
    def __init__(self):
        self.clock = 0
        self.minute = 0
        self.hour = 0
        self.day = 0
        self.week = 0
        self.month = 0
        self.year = 0
        self.hour_steps = steps['hour']
        
    def tick(self):
        self.clock += 1
        self.hour = self.clock // self.hour_steps
        # set hour to 0 when it reaches 24
        self.hour = self.hour % 24
        self.day = self.hour // 24
        self.week = self.day // 7
        self.month = self.week // 4
        self.year = self.month // 12
        
    def get_time(self):
        print(f'Clock: {self.clock}, Hour: {self.hour}, Day: {self.day}, Week: {self.week}, Month: {self.month}, Year: {self.year}')
        return self.clock, self.hour, self.day, self.week, self.month, self.year
from abc import ABC, abstractmethod
from bankcraft.agent.merchant import Clothes, Food

# from bankcraft.motivation.motivation import Motivation
from bankcraft.config import *


class MotivationState(ABC):

    def __init__(self, motivation):
        self.motivation = motivation
        self.__value = 1

    def __str__(self):
        return self.__class__.__name__

    @abstractmethod
    def set_transaction(self) -> None:
        pass

    @abstractmethod
    def set_motion(self) -> None:
        pass
    
    def get_value(self):
        return self.__value
    
    def update_value(self, amount):
        self.__value += amount

########################################


class HungerState(MotivationState):
        
    def set_transaction(self) -> None:
        self.motivation.agent.buy('hunger')
        self.update_value(-hunger_rate)

    def set_motion(self) -> None:
        self.motivation.agent.target_location = self.motivation.agent.get_nearest(Food).pos


#################################################


class FatigueState(MotivationState):

    def set_transaction(self) -> None:
        return
    def set_motion(self) -> None:
        self.motivation.agent.target_location = self.motivation.agent.home
        self.update_value(-fatigue_rate)

####################################################


class ConsumerismState(MotivationState):

    def set_transaction(self) -> None:
        self.motivation.agent.buy('consumerism')
        self.update_value(-consumerism_rate)

    def set_motion(self) -> None:
        self.motivation.agent.target_location = self.motivation.agent.get_nearest(Clothes).pos

##################################################


class SocialState(MotivationState):

    def set_transaction(self) -> None:
        if self.motivation.agent.pos == self.motivation.agent.best_friend.pos:
            self.motivation.agent.pay(20, self.motivation.agent.best_friend, 'ACH', 'social')
            self.update_value(-social_rate)

    def set_motion(self) -> None:
        self.motivation.agent.target_location = self.motivation.agent.best_friend.pos
###################################################


class WorkState(MotivationState):

    def set_transaction(self) -> None:
        return
    
    def set_motion(self) -> None:
        self.motivation.agent.target_location = self.motivation.agent.work
        self.update_value(-work_rate)

###################################################


class NeutralState(MotivationState):

    def set_transaction(self) -> None:
        #print('no txn in Neutral state')
        return
    
    def set_motion(self) -> None:
        #print('no motion in Neutral state')
        return
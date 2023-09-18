from abc import ABC, abstractmethod

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
        print(self.__value)

########################################


class HungerState(MotivationState):
        
    def switch_state(self):
        self.motivation.state = FatigueState(self.motivation)

    def set_transaction(self) -> None:
        # amount = self.person.buy('hunger')
        print('go and buy something to eat')
        self.motivation.update_motivation('hunger', -hunger_rate)

    def set_motion(self) -> None:
        print('move to the closest restaurant')

#################################################


class FatigueState(MotivationState):

    def set_transaction(self) -> None:
        # self.person.rest()
        print('too tired to do any transactions')
        self.motivation.update_motivation('fatigue', -fatigue_rate)

    def set_motion(self) -> None:
        print('go home and rest')
        # self.person._target_location = self.person.home

####################################################


class ConsumerismState(MotivationState):

    def set_transaction(self) -> None:
        print('go and buy some stuff')
        # amount = self.person.buy('consumerism')
        self.motivation.update_motivation('consumerism', consumerism_rate)

    def set_motion(self) -> None:
        print('go to the closest merchant')

##################################################


class SocialState(MotivationState):

    def set_transaction(self) -> None:
        print('pay some money to your best_Friend')
        # amount = self.person.socialize()
        self.motivation.update_motivation('social', amount=20)
        # self.person.best_friend.motivation.update_motivation('social', amount)

    def set_motion(self) -> None:
        print('visit your best_friend')
        # self.person._target_location = self.best_friend.pos
###################################################


class WorkState(MotivationState):

    def set_transaction(self) -> None:
        # self.person.work()
        print('work work work')
        self.motivation.update_motivation('work', -work_rate)

    def set_motion(self) -> None:
        print('go to work place')
        # self.person._target_location = self.person.work

###################################################


class NeutralState(MotivationState):

    def set_transaction(self) -> None:
        print('no txn in Neutral state')

    def set_motion(self) -> None:
        print('no motion in Neutral state')

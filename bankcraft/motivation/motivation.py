from __future__ import annotations
from bankcraft.config import *
from bankcraft.motivation.motivation_state import *


class Motivation:

    def __init__(self, state) -> None:
        self._state = state
        self.hunger = 1
        self.fatigue = 1
        self.social = 1
        self.work = 1
        self.consumerism = 1
        self.motivation_list = ['hunger', 'fatigue', 'social', 'consumerism', 'work']
        self.set_state(NeutralState(self))
        self.critical_motivation = None

    def set_state(self, state: MotivationState):
        self._state = state
        self._state.motivation = self

    def set_motion(self):
        self._state.set_motion()

    def set_transaction(self):
        self._state.set_transaction()

    def __str__(self):
        return str(self._state)

    def update_motivation(self, key, amount):
        if hasattr(self, key):
            setattr(self, key, getattr(self, key) + amount)
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

    def present_state(self):
        return self._state

    def live(self):
        self.update_motivation('hunger', 100*hunger_rate)
        self.update_motivation('fatigue', 100*fatigue_rate)
        self.update_motivation('social', 100*social_rate)
        self.update_motivation('consumerism', 10*consumerism_rate)

    def step(self):
        self.live()
        self.critical_motivation = self.get_critical_motivation()
        print('The critical motivation is: ', self.critical_motivation)
        if self.critical_motivation == 'hunger':
            self.set_state(HungerState(self))
        elif self.critical_motivation == 'fatigue':
            self.set_state(FatigueState(self))
        elif self.critical_motivation == 'consumerism':
            self.set_state(ConsumerismState(self))
        elif self.critical_motivation == 'social':
            self.set_state(SocialState(self))
        elif self.critical_motivation == 'work':
            self.set_state(WorkState(self))

        print(f"{self}")
        self.set_transaction()
        self.set_motion()

import random

import pytest
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.model import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from bankcraft.agent.bank import Bank
from bankcraft.agent.employer import Employer
from bankcraft.agent.person import Person
from mesa.space import MultiGrid
from bankcraft.agent.merchant import Merchant

model = Model()
initial_money = 500
model.schedule = RandomActivation(model)


def test_put_employers_in_model():
    model._put_employers_in_model()
    assert len([agent for agent in model.schedule.agents if isinstance(agent, Employer)]) == model._num_employers


def test_put_people_in_model():
    model._put_people_in_model(initial_money)
    assert len([agent for agent in model.schedule.agents if isinstance(agent, Person)]) == model._num_people


def test_put_merchant_in_model():
    model._put_merchants_in_model()
    assert len([agent for agent in model.schedule.agents if isinstance(agent, Merchant)]) == model._num_merchant


def test_put_banks_in_model():
    model._put_banks_in_model()
    assert len([agent for agent in model.schedule.agents if isinstance(agent, Bank)]) == model._num_banks


def test_employers_are_not_on_grid():
    employers_list = [agent for agent in model.schedule.agents if isinstance(agent, Employer)]
    random_employer = random.choice(employers_list) if employers_list != [] else None
    assert random_employer not in model.get_all_agents_on_grid()


def test_people_are_on_grid():
    if model.schedule.agents:
        for agent in model.schedule.agents:
            model.schedule.remove(agent)
    model._put_people_in_model(initial_money)
    people_list = [agent for agent in model.schedule.agents if isinstance(agent, Person)]
    random_person = random.choice(people_list)
    assert random_person in model.get_all_agents_on_grid()






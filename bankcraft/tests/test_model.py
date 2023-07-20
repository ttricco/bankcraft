# from mesa import Model
import pytest
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.model import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from bankcraft.agent.bank import Bank
from bankcraft.agent.employer import Employer
from mesa.space import MultiGrid
import random

model = Model()
initial_money = 500
model._num_people = 50
model._num_employers = 3
num_banks = 1
model.grid = MultiGrid(width=50, height=50, torus=False)
model.schedule = RandomActivation(model)
model.datacollector = DataCollector()


@pytest.fixture
def agent():
    return GeneralAgent(model)


@pytest.fixture
def banks():
    model.banks = [Bank(model) for _ in range(num_banks)]
    return model.banks


@pytest.fixture
def employers(banks):
    model.employers = [Employer(model) for _ in range(model._num_employers)]
    return model.employers


# it will pass if we ignore the parts related to the grid placements of the agents
# as that needs random method
def test_put_people_in_model(agent, banks, employers):
    initial_num_agents = len(model.schedule.agents)
    model._put_people_in_model(initial_money)
    final_num_agents = len(model.schedule.agents)
    assert initial_num_agents == 0 and final_num_agents == model._num_people + model._num_employers


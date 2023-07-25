from bankcraft.model import Model
from mesa.time import RandomActivation
from bankcraft.agent.bank import Bank
from bankcraft.agent.employer import Employer
from bankcraft.agent.person import Person
from bankcraft.agent.merchant import Merchant

initial_money = 500


def test_put_employers_in_model():
    model0 = Model()
    model0.schedule = RandomActivation(model0)
    model0._put_employers_in_model()
    assert len([agent for agent in model0.schedule.agents if isinstance(agent, Employer)]) == model0._num_employers


def test_put_people_in_model():
    model1 = Model()
    model1.schedule = RandomActivation(model1)
    model1._put_people_in_model(initial_money)
    assert len([agent for agent in model1.schedule.agents if isinstance(agent, Person)]) == model1._num_people


def test_put_merchant_in_model():
    model2 = Model()
    model2.schedule = RandomActivation(model2)
    model2._put_merchants_in_model()
    assert len([agent for agent in model2.schedule.agents if isinstance(agent, Merchant)]) == model2._num_merchant


def test_put_banks_in_model():
    model3 = Model()
    model3.schedule = RandomActivation(model3)
    model3._put_banks_in_model()
    assert len([agent for agent in model3.schedule.agents if isinstance(agent, Bank)]) == model3._num_banks


def test_employers_are_not_on_grid():
    model4 = Model()
    model4.schedule = RandomActivation(model4)
    employers_list = [agent for agent in model4.schedule.agents if isinstance(agent, Employer)]
    assert all(agent not in model4.get_all_agents_on_grid() for agent in employers_list)


def test_people_are_on_grid():
    model5 = Model()
    model5.schedule = RandomActivation(model5)
    model5._put_people_in_model(initial_money)
    people_list = [agent for agent in model5.schedule.agents if isinstance(agent, Person)]
    assert all(agent in model5.get_all_agents_on_grid() for agent in people_list)






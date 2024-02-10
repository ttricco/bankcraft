from bankcraft.bankcraftmodel import BankCraftModel
from mesa.time import RandomActivation
from bankcraft.agent.employer import Employer
from bankcraft.agent.bank import Bank
from bankcraft.agent.person import Person
from bankcraft.agent.merchant import Merchant
from bankcraft.agent.business import Business

initial_money = 500


def test_put_employers_in_model():
    model0 = BankCraftModel()
    model0.schedule = RandomActivation(model0)
    model0._put_employers_in_model()
    assert len([agent for agent in model0.schedule.agents if isinstance(agent, Employer)]) == model0._num_employers


def test_put_people_in_model():
    model1 = BankCraftModel()
    model1.schedule = RandomActivation(model1)
    model1._put_people_in_model(initial_money)
    assert len([agent for agent in model1.schedule.agents if isinstance(agent, Person)]) == model1._num_people


def test_put_food_merchant_in_model():
    model2 = BankCraftModel()
    model2.schedule = RandomActivation(model2)
    model2._put_food_merchants_in_model()
    assert len([agent for agent in model2.schedule.agents if isinstance(agent, Merchant)]) == model2._num_merchant


def test_put_clothes_merchant_in_model():
    model3 = BankCraftModel()
    model3.schedule = RandomActivation(model3)
    model3._put_clothes_merchants_in_model()
    assert len([agent for agent in model3.schedule.agents if isinstance(agent, Merchant)]) == model3._num_merchant//2


def test_put_food_and_clothes_merchant_in_model():
    model4 = BankCraftModel()
    model4.schedule = RandomActivation(model4)
    model4._put_food_merchants_in_model()
    model4._put_clothes_merchants_in_model()
    assert len([agent for agent in model4.schedule.agents if isinstance(agent, Merchant)]) == \
           model4._num_merchant + model4._num_merchant//2


def test_people_are_on_grid():
    model5 = BankCraftModel()
    model5.schedule = RandomActivation(model5)
    model5._put_people_in_model(initial_money)
    people_list = [agent for agent in model5.schedule.agents if isinstance(agent, Person)]
    assert all(agent in model5.get_all_agents_on_grid() for agent in people_list)


def test_banks_are_neither_in_scheduler_nor_on_grid():
    model6 = BankCraftModel()
    model6.schedule = RandomActivation(model6)
    banks_in_scheduler = [agent for agent in model6.schedule.agents if isinstance(agent, Bank)]
    banks_on_grid = [agent for agent in model6.get_all_agents_on_grid() if isinstance(agent, Bank)]
    assert len(banks_in_scheduler) == 0 and len(banks_on_grid) == 0


def test_businesses_are_neither_in_scheduler_nor_on_grid():
    model7 = BankCraftModel()
    model7.schedule = RandomActivation(model7)
    businesses_in_scheduler = [agent for agent in model7.schedule.agents if isinstance(agent, Business)]
    businesses_on_grid = [agent for agent in model7.get_all_agents_on_grid() if isinstance(agent, Business)]
    assert len(businesses_in_scheduler) == 0 and len(businesses_on_grid) == 0


def test_can_run_model():
    model = BankCraftModel(num_people=100, initial_money=1000, num_banks=1, width=50, height=50)
    current_time = model.current_time
    model.run(1)
    assert model.current_time == current_time + model._one_step_time


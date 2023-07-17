import pytest
from bankcraft.model import Model
from bankcraft.agent.person import Person
from bankcraft.agent.employer import Employer
from bankcraft.agent.bank import Bank
from bankcraft.steps import steps
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


model = Model
num_banks = 1
model.schedule = RandomActivation(model)
model.datacollector = \
    DataCollector(tables={"transactions": ["sender", "receiver", "amount", "step", "txn_id",
                                           "txn_type", "sender_account_type", "description"]})

@pytest.fixture
def person():
    return Person(model, 500)


@pytest.fixture
def employers(banks):
    model.employers = [Employer(model) for _ in range(1)]
    return model.employers


@pytest.fixture
def banks():
    model.banks = [Bank(model) for _ in range(num_banks)]
    return model.banks


def test_add_employee(employers, person, banks):
    initial_num_employees = len(employers[0].employees)
    employers[0].add_employee(person)
    assert len(employers[0].employees) == initial_num_employees + 1


def test_remove_employee(employers, person, banks):
    employers[0].add_employee(person)
    second_person = Person(model, 500)
    third_person = Person(model, 500)
    employers[0].add_employee(second_person)
    employers[0].add_employee(third_person)
    initial_num_employees = len(employers[0].employees)
    employers[0].remove_employee(second_person)
    final_num_employees = len(employers[0].employees)
    assert initial_num_employees == 3 and final_num_employees == 2


def test_pay_period_is_biweekly_or_month(employers):
    assert employers[0].pay_period == steps['biweekly'] or employers[0].pay_period == steps['month']


def test_after_30weeks_is_pay_date(employers):
    step = 30/2 * steps['biweekly']
    assert employers[0].is_pay_date(step)


def test_pay_salary_changes_the_employees_wealth(employers, person, banks):
    employers[0].add_employee(person)
    person.bank_accounts = person.assign_bank_account(model, 10)
    person.update_wealth()
    employees_initial_wealth = person.wealth
    employers[0].pay_salary()
    assert person.wealth > employees_initial_wealth


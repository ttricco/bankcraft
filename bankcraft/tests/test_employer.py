import pytest
from bankcraft.model import Model
from bankcraft.agent.person import Person
from bankcraft.agent.employer import Employer
from bankcraft.agent.bank import Bank
from bankcraft.config import steps
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import datetime

num_banks = 1
Model.schedule = RandomActivation(Model)
Model.datacollector = \
    DataCollector(tables={"transactions": ["sender", "receiver", "amount", "step", "date_time", "txn_id",
                                           "txn_type", "sender_account_type", "description"]})
Model.start_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
Model.current_time = Model.start_time


@pytest.fixture
def person():
    return Person(Model, 500)


@pytest.fixture
def employers(banks):
    Model.employers = [Employer(Model) for _ in range(1)]
    return Model.employers


@pytest.fixture
def banks():
    Model.banks = [Bank(Model) for _ in range(num_banks)]
    return Model.banks


def test_add_employee(employers, person, banks):
    initial_num_employees = len(employers[0].employees)
    employers[0].add_employee(person)
    assert len(employers[0].employees) == initial_num_employees + 1


def test_remove_employee(employers, person, banks):
    employers[0].add_employee(person)
    second_person = Person(Model, 500)
    third_person = Person(Model, 500)
    employers[0].add_employee(second_person)
    employers[0].add_employee(third_person)
    initial_num_employees = len(employers[0].employees)
    employers[0].remove_employee(second_person)
    final_num_employees = len(employers[0].employees)
    assert initial_num_employees == 3 and final_num_employees == 2


def test_pay_period_is_biweekly_or_month(employers):
    assert employers[0].pay_period == steps['biweekly'] or employers[0].pay_period == steps['month']


def test_15biweekly_is_7months_pay_date(employers):
    step = 30/2 * steps['biweekly']
    assert employers[0].is_pay_date(step)


def test_pay_salary_changes_the_employees_wealth(employers, person, banks):
    employers[0].add_employee(person)
    person.bank_accounts = person.assign_bank_account(Model, 10)
    person.update_wealth()
    employees_initial_wealth = person.wealth
    employers[0].pay_salary()
    assert person.wealth == employees_initial_wealth + person.salary_per_pay


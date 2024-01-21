import pytest
from bankcraft.bankcraftmodel import BankCraftModel
from bankcraft.agent.person import Person
from bankcraft.agent.employer import Employer
from bankcraft.agent.bank import Bank
from bankcraft.agent.business import Business
from bankcraft.config import steps
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import datetime

num_banks = 1
BankCraftModel.schedule = RandomActivation(BankCraftModel)
BankCraftModel.datacollector = \
    DataCollector(tables={"transactions": ["sender", "receiver", "amount", "step", "date_time", "txn_id",
                                           "txn_type", "sender_account_type", "description"]})
BankCraftModel.start_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
BankCraftModel.current_time = BankCraftModel.start_time


@pytest.fixture
def person():
    return Person(BankCraftModel, 500)


@pytest.fixture
def employers(banks, invoicer):
    BankCraftModel.employers = [Employer(BankCraftModel) for _ in range(1)]
    return BankCraftModel.employers


@pytest.fixture
def banks():
    BankCraftModel.banks = [Bank(BankCraftModel) for _ in range(num_banks)]
    return BankCraftModel.banks


@pytest.fixture
def invoicer():
    business_types = ["rent/mortgage", "utilities", "subscription", "membership", "net_providers"]
    BankCraftModel.invoicer = {b_type: Business(BankCraftModel, b_type) for b_type in business_types}
    return BankCraftModel.invoicer


def test_add_employee(employers, person):
    initial_num_employees = len(employers[0].employees)
    employers[0].add_employee(person)
    assert len(employers[0].employees) == initial_num_employees + 1


def test_remove_employee(employers, person):
    employers[0].add_employee(person)
    second_person = Person(BankCraftModel, 500)
    third_person = Person(BankCraftModel, 500)
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
    person.bank_accounts = person.assign_bank_account(BankCraftModel, 10)
    person.update_wealth()
    employees_initial_wealth = person.wealth
    employers[0].pay_salary()
    assert person.wealth == employees_initial_wealth + person.salary_per_pay


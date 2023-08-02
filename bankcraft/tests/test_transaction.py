from bankcraft.transaction import Transaction
from bankcraft.agent.person import Person
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.bank import Bank
from bankcraft.model import Model
import pytest
from mesa.time import RandomActivation


Model.schedule = RandomActivation(Model)
account_initial_balance = 1500
num_banks = 1
txn_amount = 300

@pytest.fixture
def agent():
    return GeneralAgent(Model)


@pytest.fixture
def banks():
    Model.banks = [Bank(Model) for _ in range(num_banks)]
    return Model.banks


def test_do_transaction(agent, banks):
    agent.bank_accounts = agent.assign_bank_account(Model, account_initial_balance)
    agent.update_wealth()
    agents_initial_wealth = agent.wealth
    another_agent = GeneralAgent(Model)
    another_agent.bank_accounts = agent.assign_bank_account(Model, account_initial_balance)
    another_agent.update_wealth()
    another_agents_initial_wealth = another_agent.wealth
    transaction = Transaction(agent,
                              another_agent,
                              txn_amount,
                              agent.txn_counter,
                              txn_type='ACH')
    transaction.do_transaction()
    agents_wealth = agent.wealth
    another_agents_wealth = another_agent.wealth
    assert (agents_initial_wealth != agents_wealth and
            agents_initial_wealth + another_agents_initial_wealth == agents_wealth + another_agents_wealth)

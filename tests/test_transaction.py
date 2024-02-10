from bankcraft.banking.transaction import Transaction
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.bank import Bank
from bankcraft.bankcraftmodel import BankCraftModel
import pytest
from mesa.time import RandomActivation


account_initial_balance: int = 1500
num_banks = 1
txn_amount = 300


@pytest.fixture
def agent():
    return GeneralAgent(BankCraftModel)


@pytest.fixture
def banks():
    BankCraftModel.banks = [Bank(BankCraftModel) for _ in range(num_banks)]
    return BankCraftModel.banks


def test_do_transaction_changes_senders_and_receivers_wealth(agent, banks):
    agent.bank_accounts = agent.assign_bank_account(BankCraftModel, account_initial_balance)
    agents_initial_wealth = agent.wealth
    another_agent = GeneralAgent(BankCraftModel)
    another_agent.bank_accounts = agent.assign_bank_account(BankCraftModel, account_initial_balance)
    another_agents_initial_wealth = another_agent.wealth
    transaction = Transaction(agent,
                              another_agent,
                              txn_amount,
                              agent.txn_counter,
                              txn_type='ACH')
    transaction.do_transaction()
    assert agents_initial_wealth == account_initial_balance and \
           agent.wealth == agents_initial_wealth - txn_amount and \
           agents_initial_wealth + another_agents_initial_wealth == agent.wealth + another_agent.wealth

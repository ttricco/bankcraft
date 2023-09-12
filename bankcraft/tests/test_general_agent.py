import pandas as pd
import pytest

from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.model import Model
from bankcraft.agent.bank import Bank
from bankcraft.agent.business import Business

from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import datetime

account_initial_balance = 1500
num_banks = 1
txn_amount = 300
Model.schedule = RandomActivation(Model)
Model.datacollector = \
    DataCollector(tables={"transactions": ["sender", "receiver", "amount", "step", "date_time", "txn_id",
                                           "txn_type", "sender_account_type", "description"]})
Model.start_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
Model.current_time = Model.start_time


@pytest.fixture
def banks():
    Model.banks = [Bank(Model) for _ in range(num_banks)]
    return Model.banks


@pytest.fixture
def agent():
    return GeneralAgent(Model)


@pytest.fixture
def other_agent():
    return GeneralAgent(Model)


@pytest.fixture
def model(banks):
    model = Model()
    return model


def test_bank_account_is_none_before_assigning(agent):
    assert agent.bank_accounts is None


def test_bank_account_is_not_none_after_assigning(agent, model):
    agent.bank_accounts = agent.assign_bank_account(model, account_initial_balance)
    assert agent.bank_accounts is not None


def test_update_wealth_is_needed_after_assigning_bank_account(agent, model):
    agent_default_wealth = agent.wealth
    agent.bank_accounts = agent.assign_bank_account(model, account_initial_balance)
    agent_wealth_before_update = agent.wealth
    agent.update_wealth()
    assert (agent_default_wealth == 0 and agent_wealth_before_update == agent_default_wealth and
            agent.wealth == num_banks*account_initial_balance)


def test_pay_changes_wealth(agent, other_agent, banks):
    agent.bank_accounts = agent.assign_bank_account(Model, account_initial_balance)
    other_agent.bank_accounts = other_agent.assign_bank_account(Model, account_initial_balance)
    agent.pay(txn_amount, other_agent, "cash", "gift")
    assert (agent.wealth == num_banks * account_initial_balance - txn_amount and
            other_agent.wealth == num_banks * account_initial_balance + txn_amount)


def test_undefined_tnx_type_does_not_change_wealth(agent, other_agent, banks):
    agent.bank_accounts = agent.assign_bank_account(Model, account_initial_balance)
    agent.update_wealth()
    agents_initial_wealth = agent.wealth
    other_agent.bank_accounts = other_agent.assign_bank_account(Model, account_initial_balance)
    other_agent.update_wealth()
    other_agent_initial_wealth = other_agent.wealth
    agent.pay(txn_amount, other_agent, "e-transfer", "gift")
    assert agents_initial_wealth == agent.wealth and other_agent_initial_wealth == other_agent.wealth


def test_updating_txn_records(agent, other_agent, banks):
    Model.datacollector = \
        DataCollector(tables={"transactions": ["sender", "receiver", "amount", "step", "date_time", "txn_id",
                                               "txn_type", "sender_account_type", "description"]})
    agent.update_records(other_agent, txn_amount, "cheque", "chequing", "debt")
    Model.datacollector.collect(Model)
    expected_txn_data = {
        "sender": agent.unique_id,
        "receiver": other_agent.unique_id,
        "amount": txn_amount,
        "step": 0,
        "date_time": Model.current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "txn_id": f"{str(agent.unique_id)}_{str(agent.txn_counter)}",
        "txn_type": "cheque",
        "sender_account_type": "chequing",
        "description": "debt",
    }
    model_txn_data = Model.datacollector.get_table_dataframe("transactions").iloc[0]
    pd.testing.assert_series_equal(pd.Series(expected_txn_data, name=0), model_txn_data)

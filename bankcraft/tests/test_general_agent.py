from unittest import TestCase
from bankcraft.model import Model
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.bank import Bank
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import pandas as pd


class TestGeneralAgent(TestCase):
    def setUp(self):
        self.model = Model
        self.agent1 = GeneralAgent(self.model)
        self.num_banks = 1
        self.num_account_types = 3
        self.account_initial_balance = 500
        self.model.banks = [Bank(self.model) for _ in range(self.num_banks)]
        self.agent1.bank_accounts = self.agent1.assign_bank_account(self.model, self.account_initial_balance)
        self.agent2 = GeneralAgent(self.model)
        self.model.schedule = RandomActivation(self.model)
        self.model.datacollector = \
            DataCollector(tables={"transactions": ["sender", "receiver", "amount", "step", "txn_id", "txn_type", "txn_account", "description"]})

    def test_assign_bank_account(self):
        self.assertIsNotNone(self.agent1.bank_accounts)

    def test_update_wealth(self):
        self.assertEqual(self.agent2.wealth, 0)
        self.agent2.bank_accounts = self.agent2.assign_bank_account(self.model, self.account_initial_balance)
        self.agent2.update_wealth()
        self.assertEqual(self.agent2.wealth, self.num_banks*self.num_account_types*self.account_initial_balance)

    def test_pay(self):
        self.agent2.bank_accounts = self.agent2.assign_bank_account(self.model, self.account_initial_balance)
        self.agent1.pay(300, self.agent2, "cash", "gift")
        self.assertEqual(self.agent1.wealth, 1200)
        self.assertEqual(self.agent2.wealth, 1800)

        with self.assertRaises(ValueError):
            self.agent1.pay(300, self.agent2, "cash", "gift")

        with self.assertRaises(Exception):
            self.agent1.pay(100, self.agent2, "e-transfer", "gift")

    def test_update_records(self):
        self.agent1.update_records(self.agent2, 100, "cheque", "debt")
        self.model.datacollector.collect(self.model)
        expected_transaction_data = {
            "sender": self.agent1.unique_id,
            "receiver": self.agent2.unique_id,
            "amount": 100,
            "step": 0,
            "txn_id": f"{str(self.agent1.unique_id)}_{str(self.agent1.txn_counter)}",
            "txn_type": "cheque",
            "description": "debt",
        }
        actual_transaction_data = self.model.datacollector.get_table_dataframe("transactions").iloc[0]
        pd.testing.assert_series_equal(pd.Series(expected_transaction_data, name=0), actual_transaction_data)

    if __name__ == '__main__':
        TestCase.main()

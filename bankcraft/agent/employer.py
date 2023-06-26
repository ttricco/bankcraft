from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.transaction import *
from bankcraft.bank_account import BankAccount


class Employer(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pay_period = 14
        self.employees = []
        self.initial_fund = 1000000
        self.bank_accounts = self.assign_bank_account(model, self.initial_fund)

    def pay_salary(self, employee, amount, date):
        if date % self.pay_period == 0:
            transaction = Cheque(self.bank_accounts[0][0],
                                 employee.bank_accounts[0][0],
                                 amount, self.model.schedule.steps + 1,
                                 self.unique_id)
            transaction.do_transaction()
            self.model.transactions.append(transaction)

    def step(self):
        for i in self.employees:
            self.pay_salary(i, i.salary, self.model.schedule.steps)

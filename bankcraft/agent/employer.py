from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.transaction import *
from bankcraft.config import steps
import random


class Employer(GeneralAgent):
    def __init__(self, model):
        super().__init__(model)
        self.pay_period = random.choice([steps['biweekly'], steps['month']])
        self.employees = []
        self.initial_fund = 1000000
        self.bank_accounts = self.assign_bank_account(model, self.initial_fund)
        # These are for use of agent reporter and needs to be handled better in the future
        self.wealth = self.initial_fund
        self.motivation = None
        self._work = None

    @property
    def work(self):
        return self._work

    @work.setter
    def work(self, value):
        self._work = value

    def is_pay_date(self, date):
        return date % self.pay_period == 0

    def step(self):
        if self.is_pay_date(self.model.schedule.steps):
            self.pay_salary()

    def add_employee(self, person):
        self.employees.append(person)

    def remove_employee(self, person):
        self.employees.remove(person)

    def pay_salary(self):
        for i in self.employees:
            self.pay(i.salary_per_pay, i, 'cheque', 'salary')


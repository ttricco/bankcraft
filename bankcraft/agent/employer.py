from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.agent.person import Person
from bankcraft.transaction import *
from bankcraft.config import steps
import random


class Employer(GeneralAgent):
    def __init__(self, model):
        super().__init__(model)
        self.pay_period = random.choice([steps['biweekly'], steps['month']])
        self._num_pays_per_year = steps['year'] // self.pay_period

        self.employees = [] # list of [person, salary, salary_per_pay]
        self._initial_fund = 1000000
        self.bank_accounts = self.assign_bank_account(model, self._initial_fund)
        # These are for use of agent reporter and needs to be handled better in the future
        self.wealth = self._initial_fund
        self.type = 'employer'
        self._location = None
        self._salary_list = [['0', '0.8', '18>', '100-200'],
                             ['1', '0.9', '18>', '54-120'],
                             ['2', '0.8', '18>', '66-96'],
                             ['3', '0.8', '18>', '49-63'],
                             ['4', '0.9', '18>', '30-60']] #['Group', 'wage_Gap_Rate', 'Age', 'Salary_Range']
        
                             
        

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    def is_pay_date(self, date):
        return date % self.pay_period == 0

    def step(self):
        if self.is_pay_date(self.model.schedule.steps):
            self.pay_salary()

    def add_employee(self, person):
        salary = self.assign_salary(person)
        salary_per_pay = salary / self._num_pays_per_year
        self.employees.append([person, salary, salary_per_pay])
        person.assign_salary_info(self,salary)

    def remove_employee(self, person):
        self.employees.remove(person)

    def pay_salary(self):
        for i in self.employees:
            person = i[0]
            salary_per_pay = i[2]
            self.pay(salary_per_pay,person , 'cheque', 'salary')


    def assign_salary(self, person):
        salary_group = random.randint(0,4)
        salary_range = self._salary_list[salary_group][3].split('-')
        salary = random.randint(int(salary_range[0]), int(salary_range[1]))
        salary = salary * 1000
        
        return salary

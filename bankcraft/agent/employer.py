from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.transaction import Transaction


class Employer(GeneralAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pay_period = 14
        self.employees = []
        self.bank_accounts = None

    def pay_salary(self, employee, amount, date):
        if date % self.pay_period == 0:
            transaction = Transaction.Cheque(self.bank_accounts,
                                             employee.bank_accounts[1],
                                             amount, self.model.schedule.steps + 1,
                                             self.unique_id)
            transaction.do_transaction()
            self.model.transactions.append(transaction)

    def step(self):
        for i in self.employees:
            # print(i.bank_accounts[1])
            self.pay_salary(i, i.salary, self.model.schedule.steps)

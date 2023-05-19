from model import Model

INITIAL_MONEY = 1000
SPENDING_PROB = 0.5 
SPENDING_AMOUNT = 100
NUM_PEOPLE = 10
SALARY = 1000
NUM_STEPS = 10

model = Model(NUM_PEOPLE, INITIAL_MONEY, 
                 SPENDING_PROB, SPENDING_AMOUNT,
                 SALARY)

for i in range(NUM_STEPS):
    model.step()

agent_money = model.datacollector.get_agent_vars_dataframe()

print(agent_money.xs(9, level="Step")["Money"])

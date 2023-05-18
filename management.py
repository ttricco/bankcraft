from model import Model

INITIAL_MONEY = 1000
SPENDING_PROB = 0.5 
SPENDING_AMOUNT = 100
NUM_PEOPLE = 10

modelTest = Model(NUM_PEOPLE, INITIAL_MONEY, 
                 SPENDING_PROB, SPENDING_AMOUNT)

for i in range(NUM_PEOPLE):
    modelTest.step()

agent_money = modelTest.datacollector.get_agent_vars_dataframe()

print(agent_money)

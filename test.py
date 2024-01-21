from bankcraft.bankcraftmodel import BankCraftModel
import pandas as pd
import time

t1 = time.time()

model = BankCraftModel(num_people=100, num_merchant=10, initial_money=1000,
                       num_employers=2, num_banks=1, width=50, height=50)
# 1 day = 144 steps
# 1 month = 30 * 144  
model.run(30 * 144 *12 )
#vis = bankcraft.utils.visualization.Visualization(model,steps=30*144, width=15, height=15)
t2 = time.time()
print('Time taken: ', t2-t1)
# agents = model.get_agents()
# people = model.get_people()
# transactions = model.get_transactions()


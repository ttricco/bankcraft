# BankCraft

An agent-based simulator to generate financial transaction data.

## Example

Here is a simple example of how to run BankCraft for now. 

```
import bankcraft

model = bankcraft.bankcraftmodel.BankCraftModel()

model.run(365)
transactions = model.get_transactions()
agents = model.get_agents()
vis = bankcraft.utils.visualization.Visualization(model, agents, transactions)
vis.grid_plot()
```

## Access

BankCraft is currently under development. While open source, it is not yet ready for public use.
BankCraft may only be used if explicit permission is given.

# BankCraft

An agent-based simulator to generate financial transaction data.

## Example

Here is a simple example of how to run BankCraft for now. 

```
import bankcraft

model = bankcraft.model.Model()

model.run(365)
transactions = model.get_transactions()

bankcraft.utils.draw_graph(model)
bankcraft.utils.draw_interactive_grid()
```

## Access

BankCraft is currently under development. While open source, it is not yet ready for public use.
BankCraft may only be used if explicit permission is given.

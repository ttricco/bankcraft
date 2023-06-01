# BankCraft

An agent-based simulator to generate financial transaction data.

## Example

Here is a simple example of how to run BankCraft for now. 

```
import bankcraft

model = bankcraft.Model()

df = model.run(10)

bankcraft.utils.draw_graph(model)
bankcraft.utils.draw_interactive_grid()
```

## Access

BankCraft is currently under development. While open source, it is yet ready for public use.
BankCraft may only be used if explicit permission is given.
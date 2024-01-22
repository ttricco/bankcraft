# BankCraft

An agent-based simulator to generate financial transaction data.

## Motivation

BankCraft is a tool for generating financial transaction data. It is designed to be a flexible, extensible, and easy to use tool.

## Example

Here is a simple example of how to run BankCraft for now. 

```
from bankcraft.bankcraftmodel import BankCraftModel
from bankcraft.utils.visualization import Visualization

model = BankCraftModel()

model.run(365)

vis = Visualization(model)
vis.grid_plot()
```

## Access

BankCraft is currently under development. While open source, it is not yet ready for public use.
BankCraft may only be used if explicit permission is given.

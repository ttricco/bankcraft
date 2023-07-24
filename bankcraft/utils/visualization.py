import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import mesa
from ..model import Model
from bankcraft.agent.merchant import Merchant
from ..agent.person import Person


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if type(agent) is Merchant:
        portrayal["Color"] = "Green"
        
    return portrayal



def draw_graph(model):
    fig, ax = plt.subplots(figsize=(10, 10))
    # draw the graph with labels and size of nodes proportional to wealth
    nx.draw_networkx(model.social_grid, pos=nx.spring_layout(model.social_grid),
                    labels={node:node for node in model.social_grid.nodes()}, 
                    node_size=[model.schedule.agents[node].wealth for node in model.social_grid.nodes()],ax = ax
                    ,width = [model.social_grid[u][v]['weight'] for u,v in model.social_grid.edges()])
    #save the graph    
    plt.savefig("graph.png")


def draw_interactive_grid(port):
    parameters = {"num_people": 5, "num_merchant": 2, "initial_money": 1000,
              "spending_prob": 0.5, "spending_amount": 100, "num_employers": 2, "num_banks": 1}
    grid = mesa.visualization.CanvasGrid(agent_portrayal, 50, 50, 500, 500)
    chart = mesa.visualization.ChartModule([{'Label': 'Wealth'}])
    server = mesa.visualization.ModularServer(Model,
                        [grid],
                        "BankCraft Model",
                        parameters)
    server.port = port # The default
    server.launch()




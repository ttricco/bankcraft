from model import Model
from agent import Person, Merchant
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
    }
    if type(agent) is Person:
        portrayal["color"] = "red" 
        if agent.money > 0:
            portrayal["Color"] = "green"
            portrayal["r"] = 0.5 * np.log2(agent.money)
            portrayal["Layer"] = 1
            portrayal['Money'] = agent.money
            portrayal['agent number'] = agent.social_node

    elif type(agent) is Merchant:
        portrayal["Color"] = "blue"
        portrayal["r"] = 0.5 * np.log2(agent.money)
        portrayal["Layer"] = 0
    return portrayal


def draw_graph(model):
    fig, ax = plt.subplots(figsize=(10, 10))
    # draw the graph with labels and size of nodes proportional to money
    nx.draw_networkx(model.social_grid, pos=nx.spring_layout(model.social_grid),
                     labels={node:node for node in model.social_grid.nodes()}, 
                     node_size=[model.schedule.agents[node].money for node in model.social_grid.nodes()])
     
    # save the graph    
    plt.savefig("graph.png")


def draw_interactive_grid():
    grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
    server = ModularServer(
        Model, [grid], "Money Model", {}
    )
    server.port = 8521  # The default
    server.launch()




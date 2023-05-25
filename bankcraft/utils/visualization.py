from model import Model
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        'agent number': agent.social_node,
        'Money': agent.money,
    }
    if agent.money > 0:
        portrayal["Color"] = "green"
        portrayal["r"] = 0.5 * np.log2(agent.money)
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




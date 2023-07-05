import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from ..model import Model
from bankcraft.agent.merchant import Merchant
from ..agent.person import Person


def _agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
    }
    if type(agent) is Person:
        portrayal["color"] = "red"
        if agent.wealth > 0:
            _extracted_from__agent_portrayal_9("green", portrayal, agent, 1)
            portrayal['wealth'] = agent.wealth
            portrayal['agent number'] = agent.social_node

    elif type(agent) is Merchant:
        _extracted_from__agent_portrayal_9("blue", portrayal, agent, 0)
    return portrayal


# TODO Rename this here and in `_agent_portrayal`
def _extracted_from__agent_portrayal_9(arg0, portrayal, agent, arg3):
    portrayal["Color"] = arg0
    portrayal["r"] = 0.5 * np.log2(agent.wealth)
    portrayal["Layer"] = arg3


def draw_graph(model):
    fig, ax = plt.subplots(figsize=(10, 10))
    # draw the graph with labels and size of nodes proportional to wealth
    nx.draw_networkx(model.social_grid, pos=nx.spring_layout(model.social_grid),
                    labels={node:node for node in model.social_grid.nodes()}, 
                    node_size=[model.schedule.agents[node].wealth for node in model.social_grid.nodes()],ax = ax
                    ,width = [model.social_grid[u][v]['weight'] for u,v in model.social_grid.edges()])
    #save the graph    
    plt.savefig("graph.png")


def draw_interactive_grid():
    grid = CanvasGrid(_agent_portrayal, 50, 50, 500, 500)
    server = ModularServer(
        Model, [grid], "wealth Model", {}
    )
    server.port = 8521  # The default
    server.launch()



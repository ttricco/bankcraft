from model import *
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(model):
    fig, ax = plt.subplots(figsize=(10, 10))
    # nodes as agents and edges as transactions
    G = model.G
    pos = nx.spring_layout(G)
    # node size is the amount of money
    node_size = [G.nodes()[i]['agent'][0].money for i in G.nodes()]
    # labels are the unique_id of the agent
    labels = {i:G.nodes()[i]['agent'][0].money for i in G.nodes()}
    ax.set_title("Money Distribution")
    nx.draw_networkx_nodes(G, pos, node_size=node_size)
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    # save the graph
    plt.savefig("graph.png")    




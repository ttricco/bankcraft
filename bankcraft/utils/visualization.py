import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import mesa
from ..model import Model
from bankcraft.agent.merchant import Merchant
from ..agent.person import Person
from ipywidgets import widgets, interact, interactive, fixed, interact_manual
import warnings
warnings.filterwarnings("ignore")

class visualization():
    def __init__(self, model, agents, transactions):
        self.model = model
        self.STEPS = 1008
        self.WIDTH = 50
        self.HEIGHT = 50
        self.COLORS = {"person": "red", "merchant": "black"}
        self.pallet = sns.color_palette("tab10")
        self.agents = agents
        self.transactions = transactions
        self.agentID_color = {}
        for i, agentID in enumerate(agents["AgentID"].unique()):
            if agents[agents["AgentID"] == agentID]["Agent type"].values[0] == "person":
                self.agentID_color[agentID] = self.pallet[i]
            else:
                self.agentID_color[agentID] = "black"
            
    def line_plot(self):
        fig, ax = plt.subplots(figsize=(15, 6))
        df = self.agents[self.agents["Agent type"] == "person"]
        df = df.groupby(['AgentID', 'Step']).last().reset_index()
        sns.lineplot(data=df, x="Step", y="wealth", hue="AgentID", palette=self.agentID_color, ax=ax)
        ax.set_title("Money over time")
        ax.set_ylabel("Money")
        ax.set_xlabel("Step")

        #legend outside
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
    def grid_plot(self):
        grid_df =  self.agents[~self.agents['location'].isnull()]
        grid_df['x'] = grid_df['location'].apply(lambda x: x[0])
        grid_df['y'] = grid_df['location'].apply(lambda x: x[1])
        grid_df['x'] = grid_df['x'].astype(int)
        grid_df['y'] = grid_df['y'].astype(int)
        pos = nx.spring_layout(nx.complete_graph(grid_df[grid_df['Agent type'] == 'person']['AgentID'].unique()))
        slider = widgets.IntSlider(value=10, min=1, max=self.STEPS, step=1, description='Step')
        @interact(slider=slider)
        def grid_plot(slider):
            fig, ax = plt.subplots(1,2, figsize=(15, 6))
            # extract the agents at the current step
            df = grid_df[grid_df['Step'] == slider]
            for agent in df['AgentID'].unique():
                label = df[df['AgentID']==agent]['Agent type'].values[0]
                sns.scatterplot(x='x', y='y', data=df[df['AgentID'] == agent], color=self.agentID_color[agent], label=label, ax=ax[0])

            ax[0].set_xlim(0, self.WIDTH)
            ax[0].set_ylim(0, self.HEIGHT)

            # Set plot title and labels
            ax[0].set_title('Agent Movements in the Grid')
            ax[0].set_xlabel('X-coordinate')
            ax[0].set_ylabel('Y-coordinate')


            node = df[df['Agent type'] == 'person']['AgentID'].unique()
            # edge being the transaction
            trans = self.transactions[self.transactions['step'] == slider]
            transaction_edges = []
            for _, row in trans.iterrows():
                if row['sender'] in node and row['receiver'] in node:
                    transaction_edges.append((row['sender'], row['receiver']))
            
            # complete graph edge
            edge = nx.complete_graph(node)
            # if there is a transaction between two agents, bold the edge
            
            nx.draw_networkx_nodes(node,
                                   pos=pos,
                                   node_color=[self.agentID_color[node] for node in node],
                                   node_size=[df[df['AgentID'] == node]['wealth'] for node in node],
                                   ax = ax[1])

            nx.draw_networkx_edges(edge, pos=pos, ax=ax[1])
            nx.draw_networkx_edges(edge, pos=pos, edgelist=transaction_edges, ax=ax[1], width=2.0)
            ax[1].set_title('Social Network')

            # Display the plot
            #plt.legend()
            plt.grid(True)
            plt.show()
        




import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
import numpy as np
import mesa
from ..model import Model
from bankcraft.agent.merchant import Merchant
from ..agent.person import Person
from ipywidgets import widgets, interact, interactive, fixed, interact_manual
import warnings
warnings.filterwarnings("ignore")


class Visualization:
    def __init__(self, model):
        self.model = model
        self.STEPS = 1008
        self.WIDTH = 15
        self.HEIGHT = 15
        self.pallet = sns.color_palette("tab10")
        self.agents = model.get_agents().reset_index()
        self.transactions = model.get_transactions()
        self.agentID_color = {}
        self.agentID_jitter = {}
        self.agentID_marker = {}
        self.persons = self.agents[self.agents["Agent type"] == "person"]['AgentID'].unique()
        for i, agentID in enumerate(self.agents["AgentID"].unique()):
            if self.agents[self.agents["AgentID"] == agentID]["Agent type"].values[0] == "person":
                self.agentID_color[agentID] = self.pallet[i%9]
                self.agentID_marker[agentID] = 'o'
                self.agentID_jitter[agentID] = np.random.normal(0,0.1,1)
                
            elif self.agents[self.agents["AgentID"] == agentID]["Agent type"].values[0] == "merchant":
                self.agentID_color[agentID] = 'black'
                self.agentID_marker[agentID] = 'D'
                self.agentID_jitter[agentID] = 0

            elif self.agents[self.agents["AgentID"] == agentID]["Agent type"].values[0] == "employer":
                self.agentID_color[agentID] = 'black'
                self.agentID_marker[agentID] = 's'
                self.agentID_jitter[agentID] = 0

    def line_plot(self):
        fig, ax = plt.subplots(figsize=(15, 6))
        df = self.agents[self.agents["Agent type"] == "person"]
        df = df.groupby(['AgentID', 'Step']).last().reset_index()
        sns.lineplot(data=df, x="Step", y="wealth", hue="AgentID", palette=self.agentID_color, ax=ax)
        ax.set_title("Money over time")
        ax.set_ylabel("Money")
        ax.set_xlabel("Step")
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        return fig, ax
        
    def grid_plot(self):
        grid_df = self.agents[~self.agents['location'].isnull()]
        grid_df['x'] = grid_df['location'].apply(lambda x: x[0])
        grid_df['y'] = grid_df['location'].apply(lambda x: x[1])
        grid_df['x'] = grid_df['x'].astype(int)
        grid_df['y'] = grid_df['y'].astype(int)
        pos = nx.spring_layout(nx.complete_graph(grid_df[grid_df['Agent type'] == 'person']['AgentID'].unique()))
        slider = widgets.SelectionSlider(
            options = list(grid_df['date_time'].unique()),
            description = 'Time:',
            layout={'width': '500px'},
        )

        @interact(slider=slider)
        def grid_plot(slider):
            fig, ax = plt.subplots(1, 2, figsize=(15, 6))
            # extract the agents at the current step
            df = grid_df[grid_df['date_time'] == slider]
            for agent in df['AgentID'].unique():
                label = df[df['AgentID'] == agent]['Agent type'].values[0]
                x = df[df['AgentID']==agent]['x']
                y = df[df['AgentID']==agent]['y']

                sns.scatterplot(x=x+self.agentID_jitter[agent], y=y+self.agentID_jitter[agent], data=df[df['AgentID'] == agent],
                                color=self.agentID_color[agent], 
                                marker=self.agentID_marker[agent],
                                ax=ax[0], s=100, label = label)
                ax[0].set_title('Agent Movements in the Grid')

            ax[0].set_xlim(0, self.WIDTH)
            ax[0].set_ylim(0, self.HEIGHT)
            ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.09), ncol=3)

            ax[0].set_xlabel('X-coordinate')
            ax[0].set_ylabel('Y-coordinate')

            node = df[df['Agent type'] == 'person']['AgentID'].unique()
            trans = self.transactions[self.transactions['step'] == slider]
            transaction_edges = []
            for _, row in trans.iterrows():
                if row['sender'] in node and row['receiver'] in node:
                    transaction_edges.append((row['sender'], row['receiver']))

            edge = nx.complete_graph(node)
            nx.draw_networkx_nodes(node,
                                   pos=pos,
                                   node_color=[self.agentID_color[node] for node in node],
                                   node_size=[df[df['AgentID'] == node]['wealth'] for node in node],
                                   ax=ax[1])

            nx.draw_networkx_edges(edge, pos=pos, ax=ax[1])
            nx.draw_networkx_edges(edge, pos=pos, edgelist=transaction_edges, ax=ax[1], width=2.0)
            ax[1].set_title('Social Network')

            # Display the plot
            plt.tight_layout()
            plt.grid(True)
            plt.show()

    def sender_bar_plot(self, include='all'):
        df = self.transactions[self.transactions['sender'].isin(self.persons)]
        df = df if include == 'all' else df[df['sender'] == include]
        df = df.groupby(['sender', 'description']).sum().reset_index()
        fig, ax = plt.subplots(figsize=(15, 6))
        sns.barplot(x='sender', y='amount', hue='description', data=df, ax=ax)
        for xtick in ax.get_xticklabels():
            xtick.set_color(self.agentID_color[int(xtick.get_text())])
            
        ax.set_xticklabels([f"{str(agent)[:7]}..." for agent in df.sender.unique()],
                           rotation=45, horizontalalignment='right')
        ax.set_title('Sender Bar Plot')
        ax.set_ylabel('Total Amount')
        ax.set_xlabel('Sender')
        return fig, ax

    def receiver_bar_plot(self, include='all'):
        df = self.transactions[self.transactions['receiver'].isin(self.persons)]
        df = df if include == 'all' else df[df['receiver'] == include]
        df = df.groupby(['receiver', 'description']).sum().reset_index()
        fig, ax = plt.subplots(figsize=(15, 6))
        sns.barplot(x='receiver', y='amount', hue='description', data=df, ax=ax,)

        for xtick in ax.get_xticklabels():
            xtick.set_color(self.agentID_color[int(xtick.get_text())])
        
        ax.set_xticklabels([f"{str(agent)[:7]}..." for agent in df.receiver.unique()],
                           rotation=45, horizontalalignment='right')
        ax.set_title('Receiver Bar Plot')
        ax.set_ylabel('Total Amount')
        ax.set_xlabel('Receiver')
        return fig, ax
        
    def motivation_plot(self, agentID):
        df = self.agents[self.agents['AgentID'] == agentID]
        df['date_time'] = pd.to_datetime(df['date_time'])
        df = df.set_index('date_time')
        color = self.agentID_color[agentID]
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.plot(df['consumerism level'], color='orange')
        ax.plot(df['hunger level'], color='red')
        ax.plot(df['fatigue level'], color='blue')
        ax.plot(df['social level'], color='green')
        ax.plot(df['work level'], color='m')
        ax.axhline(y=20, color='grey', linestyle='--')
        labels = ax.get_xticklabels()
        ax.set_xticklabels(labels, rotation=45)
        xticks = ax.get_xticks()
        ax.vlines(xticks, 0, 20, linestyles='dashed', colors='grey')
        ax.locator_params(axis='x', nbins=10)
        ax.set_title(f"Motivation over time for agent {agentID}")
        ax.set_ylabel("Motivation")
        ax.set_xlabel("date")
        ax.legend(['consumerism level','hunger level', 'fatigue level', 'social level', 'work level'], frameon=True)#,facecolor=color, framealpha=1)
        return fig, ax
        
    def transaction_type_bar_plot(self):
        df = self.transactions
        df = df.groupby(['txn_type']).sum().reset_index()
        fig, ax = plt.subplots(figsize=(15, 6))
        sns.barplot(x='txn_type', y='amount', data=df, ax=ax)
        ax.set_title("Transaction type")
        ax.set_ylabel("Total Amount")
        ax.set_xlabel("Transaction type")
        return fig, ax
    
    

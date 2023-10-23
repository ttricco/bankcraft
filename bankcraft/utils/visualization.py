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
import matplotlib.colors as mcolors


class Visualization:
    def __init__(self, model , steps=1008, width=15, height=15):
        self.model = model
        self.STEPS = steps
        self.WIDTH = width
        self.HEIGHT = height
        self.pallet = sns.color_palette("tab10")
        self.agents = model.get_agents().reset_index()
        self.transactions = model.get_transactions()
        self.people = model.get_people()
        self.agentID_color = {}
        self.agentID_jitter = {}
        self.agentID_marker = {}
        self.persons = self.people['AgentID'].unique()
        for i, agentID in enumerate(self.agents["AgentID"].unique()):
            if self.agents[self.agents["AgentID"] == agentID]["agent_type"].values[0] == "person":
                self.agentID_color[agentID] = self.pallet[i%9]
                self.agentID_marker[agentID] = 'o'
                self.agentID_jitter[agentID] = np.random.normal(0,0.1,1)
                
            elif self.agents[self.agents["AgentID"] == agentID]["agent_type"].values[0] == "merchant":
                self.agentID_color[agentID] = 'black'
                self.agentID_marker[agentID] = 'D'
                self.agentID_jitter[agentID] = 0

            elif self.agents[self.agents["AgentID"] == agentID]["agent_type"].values[0] == "employer":
                self.agentID_color[agentID] = 'black'
                self.agentID_marker[agentID] = 's'
                self.agentID_jitter[agentID] = 0

    def line_plot(self):
        fig, ax = plt.subplots(figsize=(15, 6))
        df = self.people
        df = df.groupby(['AgentID', 'Step']).last().reset_index()
        df['date_time'] = pd.to_datetime(df['date_time'])
        df = df.set_index('date_time')
        sns.lineplot(data=df, x="date_time", y="wealth", hue="AgentID", palette=self.agentID_color, ax=ax)
        ax.set_title("Wealth over time")
        ax.set_ylabel("Wealth")
        ax.set_xlabel("Step")
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        return fig, ax
        
    def grid_plot(self):
        grid_df = self.agents[~self.agents['location'].isnull()]
        grid_df['x'] = grid_df['location'].apply(lambda x: x[0])
        grid_df['y'] = grid_df['location'].apply(lambda x: x[1])
        grid_df['x'] = grid_df['x'].astype(int)
        grid_df['y'] = grid_df['y'].astype(int)
        pos = nx.spring_layout(nx.complete_graph(grid_df[grid_df['agent_type'] == 'person']['AgentID'].unique()))
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
                label = df[df['AgentID'] == agent]['agent_type'].values[0]
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
            node = self.people[self.people['date_time'] == slider]['AgentID'].unique()
            trans = self.transactions[self.transactions['step'] == slider]
            transaction_edges = []
            for _, row in trans.iterrows():
                if row['sender'] in node and row['receiver'] in node:
                    transaction_edges.append((row['sender'], row['receiver']))
            people = self.people[self.people['date_time'] == slider]
            edge = nx.complete_graph(node)
            nx.draw_networkx_nodes(node,
                                   pos=pos,
                                   node_color=[self.agentID_color[node] for node in node],
                                   node_size=[people[people['AgentID'] == node]['wealth'] for node in node],
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
        df = self.people[self.people['AgentID'] == agentID]
        df['date_time'] = pd.to_datetime(df['date_time'])
        df = df.set_index('date_time')
        color = self.agentID_color[agentID]
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.plot(df['ConsumerismState'], color='orange')
        ax.plot(df['HungerState'], color='red')
        ax.plot(df['FatigueState'], color='blue')
        ax.plot(df['SocialState'], color='green')
        ax.plot(df['WorkState'], color='m')
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
    
    def location_over_time(self, agentID):
        grid_df = self.agents[~self.agents['location'].isnull()]
        grid_df['x'] = grid_df['location'].apply(lambda x: x[0])
        grid_df['y'] = grid_df['location'].apply(lambda x: x[1])
        grid_df['x'] = grid_df['x'].astype(int)
        grid_df['y'] = grid_df['y'].astype(int)
        grid_df['date_time'] = pd.to_datetime(grid_df['date_time'])
        pos = nx.spring_layout(nx.complete_graph(grid_df[grid_df['agent_type'] == 'person']['AgentID'].unique()))
        slider = widgets.SelectionSlider(
            options = list(grid_df['date_time'].unique()),
            description = 'Time:',
            layout={'width': '500px'},
        )
        @interact(slider=slider)
        def plot_agent_trace(slider):
            # Filter the DataFrame for the specified agent ID
            df = grid_df[grid_df['AgentID'] == agentID]
            current_location = df[df['date_time'] == slider]
            df = df[df['date_time'] <= slider]
            fig, ax = plt.subplots(1, 1, figsize=(6, 6))
            
            min_time = df['date_time'].min()
            max_time = slider
            if min_time == max_time:
                df['alpha'] = 1
            else:
                df['alpha'] = (df['date_time'] - min_time) / (max_time - min_time)
            

            # Plot the agent's trace with varying transparency (alpha)
            sns.scatterplot(x=df['x'], y=df['y'], data=df, color=self.agentID_color[agentID], alpha=df['alpha'], ax=ax)
        
            # Plot the agent's current location as grey circle
            sns.scatterplot(x=current_location['x'], y=current_location['y'], data=current_location,
                            color=self.agentID_color[agentID],
                            marker='o',
                            ax=ax, s=100)
            # plt merchandise locations as black diamonds
            sns.scatterplot(x=grid_df[grid_df['agent_type'] == 'merchant']['x'], y=grid_df[grid_df['agent_type'] == 'merchant']['y'],
                            data=grid_df[grid_df['agent_type'] == 'merchant'], color='black', marker='D', ax=ax, s=100)
            
            # Plot employer locations as black squares
            sns.scatterplot(x=grid_df[grid_df['agent_type'] == 'employer']['x'], y=grid_df[grid_df['agent_type'] == 'employer']['y'],
                            data=grid_df[grid_df['agent_type'] == 'employer'], color='black', marker='s', ax=ax, s=100)
            
            ax.set_title('Agent Trace')
            ax.set_xlim(0, self.WIDTH)
            ax.set_ylim(0, self.HEIGHT)
            ax.set_xlabel('X-coordinate')
            ax.set_ylabel('Y-coordinate')
            
            plt.show()



    def account_balance_over_time(self, agentID):
        df = self.people[self.people['AgentID'] == agentID]
        df['date_time'] = pd.to_datetime(df['date_time'])
        df = df.groupby(['Step']).last().reset_index()
        #number of columns starting with account
        num_accounts = len([col for col in df.columns if col.startswith('account')])
        fig, ax = plt.subplots(figsize=(15, 6))
        for i in range(num_accounts):
            account_df = df[['Step', f'account_{i}']]
            sns.lineplot(data=account_df, x="Step", y=f"account_{i}", ax=ax, label=f"account_{i}")
            
        ax.legend()    
        ax.set_title(f"Account balance over time for agent {agentID}")
        ax.set_ylabel("Account balance")
        ax.set_xlabel("Step")
        plt.show()
        return fig, ax
                
    # def income_outcome_bar_plot(self, agentID):
    #     income = self.transactions[(self.transactions['description'] == 'salary') & (self.transactions['receiver'] == agentID)]
    #     outcome = self.transactions[(self.transactions['description'] != 'salary') & ( self.transactions['sender'] == agentID)].groupby(['description']).sum().reset_index()
    #     outcome['amount'] = -outcome['amount']
    #     df = pd.concat([income, outcome])
        
    #     return fig, ax
        
    def expenses_breakdown_plot(self,agentID):
        df = self.transactions[(self.transactions['sender']==agentID ) | (self.transactions['receiver']==agentID)]
        df =df.groupby('description').sum().reset_index()
        salary = df[df['description']=='salary']['amount'].values[0]
        df = df[df['description']!='salary']
        df['amount'] = df['amount'].abs().sort_values(ascending=False)
        df['percentage'] = df['amount'].apply(lambda x: x/salary)
        # just columns we need
        df = df[['description','amount','percentage']]
        # if sum of percentage is less than 1, add saving
        if df['percentage'].sum() < 1:
            # add new row
            df.loc[len(df)] = ['saving',salary - df['amount'].sum(),1-df['percentage'].sum()]
        df = df.sort_values(by='percentage',ascending=False)
        
        expenses = self.transactions.description.unique()
        expenses = np.append(expenses,['others','saving'])
        colors = list(mcolors.TABLEAU_COLORS.values())
        colors = colors[0:len(expenses)]
        colors = dict(zip(expenses, colors))

        fig, ax = plt.subplots(1,2,figsize=(15,5))
        bar = sns.barplot(x='description',y='amount',data=df,ax=ax[0],palette=colors)
        bar.set_xlabel('Expenses')
        bar.set_ylabel('Amount')
        bar.set_xticklabels(bar.get_xticklabels(),rotation=45)
        
        others = df[df['percentage']<0.10]
        df['description'] = df['description'].apply(lambda x: x if df[df['description']==x]['percentage'].values[0] > 0.10 else 'others')
        df = df.groupby('description').sum().reset_index()
        
        ax[1].pie(df['percentage'], startangle=90,colors=[colors[x] for x in df['description']],autopct='%1.1f%%',labels=df['description'])
        # show othrs with their percentage
        for i in range(len(others)):
            ax[1].text(1.5,0.5+i*0.1,f"{others.iloc[i]['description']} ({round(others.iloc[i]['percentage']*100,2)}%)",color='black')
        ax[1].axis('equal')
        ax[0].set_title('Expenses Breakdown by Amount')
        ax[1].set_title('Expenses Breakdown by Percentage of Salary')

        
        return fig, ax
    
    
    def transaction_plot(self):
        df = self.transactions.copy()
        df['date_time'] = pd.to_datetime(df['date_time'])
        df['date'] = df['date_time'].dt.date
        df['date'] = pd.to_datetime(df['date'])
        df['day'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['amount'] = df['amount'].abs()

        view_toggles_buttons = widgets.ToggleButtons(
            options=['day', 'month'],
            description='View:',
            disabled=False
        )

        metric_toggles_buttons = widgets.ToggleButtons(
            options=['number', 'amount'],
            description='Metric:',
            disabled=False
        )

        @widgets.interact(view=view_toggles_buttons, metric=metric_toggles_buttons)
        def plot(view, metric):
            fig, ax = plt.subplots(figsize=(15, 5))
            
            if view == 'day':
                data_grouped = df.groupby(['year', 'month', 'day', 'description'])
            else:
                data_grouped = df.groupby(['year', 'month', 'description'])

            if metric == 'number':
                data_to_plot = data_grouped.size().unstack(fill_value=0)
                title = 'Number of transactions per ' + view
                y_label = 'Number of transactions'
            else:
                data_to_plot = data_grouped['amount'].sum().unstack(fill_value=0)
                title = 'Amount of transactions per ' + view
                y_label = 'Amount of transactions'

            data_to_plot.plot(kind='bar', stacked=True, ax=ax)
            ax.set_xlabel('Date')
            ax.set_ylabel(y_label)
            ax.set_title(title)

            # Anchor the legend outside of the plot
            ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

            plt.show()
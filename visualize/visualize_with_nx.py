import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
data_directory = os.path.join(parent_directory, 'data/task2')

df = pd.read_csv(data_directory, sep='\t')

G = nx.from_pandas_edgelist(df, 'u_hash', 'v_hash')

nodes = list(G.nodes())
subgraph = G.subgraph(nodes)

plt.figure(figsize=(12, 12))
nx.draw(subgraph, with_labels=False, node_size=20, font_size=8)
plt.show()

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os


current_directory = os.getcwd()
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))

data_directory = os.path.join(parent_directory, 'data/task2')
data2_directory = os.path.join(parent_directory, 'data/info_for_task2.csv')

data = pd.read_csv(data_directory, sep='\t')
data2 = pd.read_csv(data_directory, sep='\t')

data["inn"] = data["inn"].map(str)

temp = data2['u_hash'].str.split(':',expand=True)
data2['request_type'] = temp[0]
data2["u_hash"] = temp[1]

# группируем данные по v_hash для каждого u_hash
data2 = data2.groupby(["u_hash"]).agg(list).reset_index()
data2["request_type"] = data2['request_type'].map(lambda x: x[0])

# превращаем в словарь, чтобы разбить потом по отдельным столбцам
def v_hash_maper(stroka):
    dictionary = {}
    for i in range(len(stroka)):
        dictionary[stroka[i].split(":")[0]] = stroka[i].split(":")[1]
    return dictionary
        
data2["v_hash"] = data2["v_hash"].map(v_hash_maper)
data2 = pd.concat([data2.drop(['v_hash'], axis=1), data2['v_hash'].apply(pd.Series)], axis=1)

# собираем список столбцов из v_hash которые можно будет использовать для построения графов
list_of_headers = list(data2.columns)
list_of_headers.remove("u_hash")
list_of_headers.remove("request_type")
list_of_headers.remove("inn")

#складываем данные из task2 и info_for_task2
data2 = data.merge(data2, on='inn', how='outer')

# достаем точки из df pandas
main_name = "main_okved_name"
data2 = data2[data2[main_name].notna()]
column_data = data2[data2["inn"].notna()]
ALL_POINTS = nx.from_pandas_edgelist(column_data, main_name , "inn")
for i in list_of_headers:
    column_data = data2[data2[i].notna()]
    #display(column_data)
    G = nx.from_pandas_edgelist(column_data, main_name , i)
    ALL_POINTS = nx.compose(ALL_POINTS, G)

    
G = ALL_POINTS

nodes = list(G.nodes())
subgraph = G.subgraph(nodes)
new_sub = G.to_directed()

# считаем центральность
degCent = nx.degree_centrality(G)

# сортируем по сентральности
degCent_sorted=dict(sorted(degCent.items(), key=lambda item: item[1],reverse=True))

# считаем количество соседей
betCent = nx.betweenness_centrality(G, normalized=True, endpoints=True)

# сортируем по количеству соседей
betCent_sorted=dict(sorted(betCent.items(), key=lambda item: item[1],reverse=True))


# берем 10 самых самых крутых точек (не более 10, цветов ограниченнное количество)
N_top=10
keys_deg_top=list(degCent_sorted)[0:N_top]
keys_bet_top=list(betCent_sorted)[0:N_top]

# потом делаем точки еще круче
inter_list = list(set(keys_deg_top) & set(keys_bet_top))


# Топ 10 отраслевых кодов по использованию в компаниях и компании их использующие:
new_data = pd.DataFrame()
G2=nx.Graph()

# передаем для записей из каждой отрасли свой цвет:
grath_colors = ["red", "green", "blue", "yellow", "orange", "pink", "purple", "cyan", "teal", "lime"]
color_map = []
last_len_loints = 0
for i in range(len(inter_list)):
    new_data = pd.concat([new_data, data2[data2["main_okved_name"] == inter_list[i]]])
    new_data = new_data[new_data["legal_name"].notna()]
    new_points = nx.from_pandas_edgelist(new_data, main_name , "legal_name")
    for j in range(len(new_points) - last_len_loints):
        color_map.append(grath_colors[i])
    last_len_loints = len(new_points)

G2 = new_points
nodes2 = list(G2.nodes())

X = 60
plt.figure(figsize=(X, X))

# задает длинну граней между узлами
df = pd.DataFrame(index=G2.nodes(), columns=G2.nodes())
for row, data in nx.shortest_path_length(G2):
    for col, dist in data.items():
        df.loc[row,col] = dist

df = df.fillna(df.max().max())
clo_center = nx.closeness_centrality(G2)
layout = nx.kamada_kawai_layout(G2, dist=df.to_dict(), weight=clo_center, scale=1000.0)


nx.draw(G2, layout, with_labels=True, node_size=3000, font_size=12, alpha=0.9, node_shape="8", node_color=color_map)
plt.show()

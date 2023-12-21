import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# типы данных которые есть в v_hash task2:

"""
array(['email', 'phone', 'domain', 'ogrn', 'inn', 'id', 'p', 'shop_id',
       'chain_id', 'host', 'publisher_name', 'content_name', 'bundle_id'],

"""

data2 = pd.read_csv('task2-Copy1 — копия — копия.csv', delimiter='\t')
data = pd.read_csv('info_for_task2-Copy1.csv', delimiter=';')
# пока inn побудет строкой, для тестов
data["inn"] = data["inn"].map(str)

# вынес тип лога u_hash в отдельный столбик, может пригодится, а может и нет
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
data2 = data.merge(data2, on='inn', how='outer')
display(data2)

# пока проверял только для inn, может выдать ошибку при значении NaN
# а еще inn могут повторяться, надо будет обязательно еще отфильтровать немного data2
data2 = data2[data2['inn'].notna()]
data2 = data2[data2['main_okved_name'].notna()]

# достаем точки из df pandas
G = nx.from_pandas_edgelist(data2, "main_okved_name", "inn")
nodes = list(G.nodes())
subgraph = G.subgraph(nodes)

# ЕСЛИ я правильно понял все inn в группе относятся к типу производства, по этим inn можно понять кто работает в данной отрасли
central_firma_list = sorted(list(nx.algorithms.community.label_propagation.asyn_lpa_communities(G)), key=len, reverse=True)
for i in central_firma_list:
    # название (okved_name) отрасли + число inn связанных с ним
    print(sorted(i, reverse=True)[0], len(i) - 1)


# выводим график
plt.figure(figsize=(12, 20))
nx.draw(subgraph, with_labels=True, node_size=10, font_size=8)
plt.show()

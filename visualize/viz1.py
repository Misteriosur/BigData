central_firma_list = sorted(list(nx.algorithms.community.label_propagation.asyn_lpa_communities(G)), key=len,
                            reverse=True)
list_of_busines = {}
for i in central_firma_list:
    # название (okved_name) отрасли + число inn связанных с ним
    sorted_busines = (sorted(i, reverse=True))
    display(sorted_busines[0], len(sorted_busines[1:]))
    if sorted_busines[0].startswith("ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ"):
        list_of_busines[sorted_busines[0]] = sorted_busines[1:]

d=isplay(len(list_of_busines))

counter_of_otrasl = {}
for i in list_of_busines.keys():
    if list(data[data["legal_name"] == i].head(1)["main_okved_name"])[0] not in counter_of_otrasl.keys():
        counter_of_otrasl[list(data[data["legal_name"] == i].head(1)["main_okved_name"])[0]] = 1
    else:
        counter_of_otrasl[list(data[data["legal_name"] == i].head(1)["main_okved_name"])[0]] += 1

inter_list = list(map(lambda x: x[0], sorted(counter_of_otrasl.items(), key=lambda x: x[1], reverse=True)[:10]))
display("Самые перспективные отрасли:", inter_list)
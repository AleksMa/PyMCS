import sys

sys.path.append(sys.argv[0][:-6] + 'VF2/')

import itertools as it
import matplotlib.cbook
import networkx as nx
import time
import warnings
from vf import Vf

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


# Все возможные сочетания узлов list_nodes размера k
def gen_combinations(list_nodes, k):
    return list(it.combinations(list_nodes, k))


# Индуцированный списком вершин подграф
def extract_induced_subgraph(graph, list_nodes):
    subgraph = graph.copy()
    listnodes = [x for x in subgraph.nodes if x not in list_nodes]
    subgraph.remove_nodes_from(listnodes)
    return subgraph


# Поиск наибольшего общего подграфа
# Возвращает тройку - (подграф в обозначениях первого графа, отображение в виде python-словаря, количество общих вершин)
def maximum_common_induced_subgraph(G1, G2, min_number_vertex=3, seconds=30.0):
    reverse = False

    if G1.number_of_nodes() > G2.number_of_nodes():
        tempG = G1
        G1 = G2
        G2 = tempG
        reverse = True

    commons = []
    now = time.time()
    i = 0
    break_flag = False

    for combination_size in [G1.number_of_nodes(), min_number_vertex] + list(
            range(min_number_vertex, G1.number_of_nodes())):
        if break_flag:
            break
        combinations = gen_combinations(G1.nodes, combination_size)

        subgraphs1 = []
        if len(combinations) == 0 or len(combinations[0]) > G2.number_of_nodes():
            if i > 0:
                break_flag = True
            continue

        for combinaison in combinations:
            graph_extracted = extract_induced_subgraph(G1, combinaison)
            if len(graph_extracted.nodes()) > 0 and nx.is_connected(graph_extracted):
                subgraphs1.append(graph_extracted)
            if time.time() - now > seconds:
                break_flag = True
                break

        for sub1 in subgraphs1:
            vf2 = Vf()
            res = vf2.main(G2, sub1)
            if res != {}:
                commons.append((sub1, res, sub1.number_of_nodes()))
                if i > 1:  # Гарантированно нашли наибольший общий подграф
                    break_flag = True
                    break
            if time.time() - now > seconds:
                break_flag = True
                break
            if i == 0 and len(commons) > 0:  # Гарантированно нашли наибольший общий подграф
                break_flag = True
                break
        if i == 1 and len(commons) == 0:  # Не нашли общий подграф минимального размера, значит и больших подграфов нет
            break
        i += 1

    highest = 0
    for tup in commons:
        if tup[2] > highest:
            highest = tup[2]

    for tup in commons:
        if tup[2] == highest:
            if reverse:  # Если ранее поменяли графы (второй граф меньше), то нужно инвертировать отображение
                map_reverse = {v: k for k, v in tup[1].items()}
                return tup[0], map_reverse, tup[2]
            return tup
    return ()

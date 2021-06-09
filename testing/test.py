import networkx as nx
import sys
from itertools import combinations, groupby
import random


def generate_random_connected_graph(n, p):
    edges = combinations(range(n), 2)
    G = nx.Graph()
    for i in range(n):
        G.add_node(i, attr=int(random.random() * 12))
    if p <= 0:
        return G
    if p >= 1:
        return nx.complete_graph(n, create_using=G)
    for _, node_edges in groupby(edges, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        G.add_edge(*random_edge, weight=int(random.random() * 2))
        for e in node_edges:
            if random.random() < p:
                G.add_edge(*e, weight=int(random.random() * 2))
    return G


size = int(sys.argv[1])
G = generate_random_connected_graph(size, 0.5)

for i in range(2):
    with open('test'+str(i+1)+'.txt', 'w') as the_file:
        H = G.copy()
        for j in range(int(random.random() * size / 2)):
            H.remove_node(j)
        the_file.write("t\n")
        for node in H.nodes():
            the_file.write("v " + str(node)  + " " + str(H.nodes[node]['attr']) + "\n")

        for edge in H.edges():
            the_file.write("e " + str(edge[0]) + " " + str(edge[1]) + " " + str(H[edge[0]][edge[1]]['weight']) + "\n")
        the_file.write("t\n")

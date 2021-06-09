#!/usr/bin/env python3
import sys
from likelihood import get_omega, check_likelihood
from mcs import *
from parser import create_graph

if len(sys.argv) < 5:
    print("sys.argv[1]: Graph file1")
    print("sys.argv[2]: Graph file2")
    print("sys.argv[3]: Mature rate")
    print("sys.argv[4]: Limit in seconds")
    print("sys.argv[5]: Likelihood")
    exit()

count = 12

G1_subgraphs = create_graph(sys.argv[1])
G2_subgraphs = create_graph(sys.argv[2])

mature_rate = float(sys.argv[3])
seconds = float(sys.argv[4])
likelihood = float(sys.argv[5])

common = 0.0
size1 = 0.0
size2 = 0.0

now = time.time()

# Собственно определение максимальных общих подграфов
for G1d in G1_subgraphs:
    I = G1d['n']
    G1 = G1d['g']
    len1 = len(G1.nodes())
    size1 += len1

    max_j = 0
    max_plag = 0.0
    max_common = {}

    omega = get_omega(G1, count)

    for G2d in G2_subgraphs:
        J = G2d['n']
        G2 = G2d['g']
        len2 = len(G2.nodes())

        if I == 0:
            size2 += len2

        if not check_likelihood(G2, count, omega, likelihood):
            continue

        mature = mature_rate * min(G1.number_of_nodes(), G2.number_of_nodes())

        commons = maximum_common_induced_subgraph(G1, G2, int(mature), seconds / 2)

        if len(commons) > 0:
            plag = float(commons[2]) / len1
            if plag > max_plag:
                max_plag = plag
                max_j = J
                max_common = commons[1]

    common += max_plag * len1

    # Заимствования по наиболее близким функциям и изоморфизм
    print(I, max_j, max_plag, "{" + (",".join("{}:{}".format(k, v) for k, v in max_common.items())) + "}")

print(common / size1)  # Общая доля заимствований

# print(int(time.time() - now))

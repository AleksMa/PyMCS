import networkx as nx


# Парсинг графа во внутреннем формате
# t
# v <vertex_number> <vertex_attribute>
# vertexes...
# e <edge_source> <edge_dest> <edge_attribute>
# edges...
# t
# another subgraphs...
def create_graph(filename):
    Gs = []
    try:
        with open(filename, "r") as fin:
            G = nx.Graph()
            line_num = -1
            for line in fin:
                lineList = line.strip().split(" ")
                if not lineList:
                    print("Class GraphSet __init__() line split error!")
                    exit()
                if lineList[0] == 't':
                    if line_num != -1 and len(G.nodes()) > 0:
                        Gs.append({'g': G, 'n': line_num})
                    line_num = line_num + 1
                    G = nx.Graph()
                if lineList[0] == 'v':
                    if len(lineList) != 3:
                        print("Class GraphSet __init__() line vertex error!")
                        exit()
                    G.add_node(int(lineList[1]), attr=lineList[2])
                elif lineList[0] == 'e':
                    if len(lineList) != 4:
                        print("Class GraphSet __init__() line edge error!")
                        exit()
                    G.add_edge(int(lineList[1]), int(lineList[2]), weight=int(lineList[3]))
                else:
                    # Пустая строка
                    continue
    except(IOError):
        print("Class GraphSet __init__() Cannot open Graph file", filename)
        exit()
    return Gs

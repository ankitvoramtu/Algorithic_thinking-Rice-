import random
import provided as pd

def computer_network (url):
   graph = pd.load_graph(url)
   return graph

def make_complete_graph(num_nodes, p): 
    """
    This function build a complete undirected graph with num_nodes
    """
    G = {}
    for i in range(num_nodes):
        G[i] = set([])
        for j in range(num_nodes):
            if i != j:
                a = random.uniform(0, 1)
                if a < p:
                    G[i].add(j)

    return G
    
def ER(num_nodes, p):
    return make_complete_graph(num_nodes, p)


def UPA(n, m):
    g = make_complete_graph(m, float("inf"))
    for i in range(m, n):
        #in_degree_g = compute_in_degrees(g)
        #totindeg = sum(list(in_degree_g.values()))
        new_neighbors = set([])
        for j in range(m):
            new_neighbors.add(random.choice(list(g.keys())))
        g[i] = new_neighbors
       # a = DPATrial (m)
        #print a.run_trial(m)
        #value = a.run_trial(m)
        #g [i] = value
    return g
    
def calculate_edges(graph):
    return sum([len(graph[node]) for node in graph])
   
"""
c = computer_network ("http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt") 
a =  ER(1347,0.0035)   
b = UPA(1347,5)
print len(a), calculate_edges(a)

print len(b), calculate_edges(b), calculate_edges(c)
"""
#print len(UPA(1348,5))
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 21:55:41 2014
For the Project component of Module 2, you will first write Python code that 
implements breadth-first search. Then, you will use this function to compute 
the set of connected components (CCs) of an undirected graph as well as 
determine the size of its largest connected component. Finally, you will write 
a function that computes the resilience of a graph (measured by the size of its
largest connected component) as a sequence of nodes are deleted from the graph.
You will use these functions in the Application component of Module 2 where you
will analyze the resilience of a computer network, modeled by a graph. As in 
Module 1, graphs will be represented using dictionaries.
"""
from collections import deque
import random
import graphs
import matplotlib.pylab as plt
import fast_target_order as ft
import provided as pd
def bfs_visited(ugraph, start_node):
    """this function return all nodes connected to start_node"""
    visited = set([start_node])
    que = deque([start_node])
    while que:
        initial_node = que.popleft()
        if initial_node in ugraph:
            if len(ugraph[initial_node]) != 0:
                neighbors = ugraph[initial_node]
                for node in neighbors:
                    if node not in visited:
                        visited.add(node)
                        que.append(node)
    return visited
    

def cc_visited(ugraph):
    """this function return connected component in graph"""
    connected_component = []
    unvisited = [dummy_node for dummy_node in ugraph]
    while unvisited:
        temp = set([])
        node = random.choice(unvisited)
        visited = bfs_visited(ugraph, node)
        temp = temp.union(visited)
        connected_component.append(temp)
        unvisited = [dummy_n for dummy_n in unvisited if dummy_n not in visited]
    return connected_component

def largest_cc_size(ugraph):
    """this function calculate the largest size of cc in graph"""
    connected_component = cc_visited(ugraph)
    if len(connected_component) == 0:
        return 0
    return max([len(dummy_c) for dummy_c in connected_component])
    
def compute_resilience(ugraph, attack_order):
    """this function measure Graph resilience"""
    sizes = [largest_cc_size(ugraph)]
    for node in attack_order:
        del ugraph[node]
        for dummy_key, values in ugraph.items():
            if node in values:
                values.remove(node)
        largest_size = largest_cc_size(ugraph) 
        sizes.append(largest_size)        
    return sizes
    
def random_attacked(graph):
    nodes = [dummy_node for dummy_node in graph]
    random.shuffle(nodes)
    return nodes

def plot_graph(graph, attacked_order):
   """plot the results as three curves combined in a single plot. 
   (Use a line plot for each curve.) The horizontal axis for your 
   single plot be the the number of nodes removed (ranging from zero to the 
   size of the graph) while the vertical axis should be the size of the largest
   connect component in the graphs resulting from the node removal.
   """
   x_axix = [dummy_node for dummy_node in graph] + [len(graph)]
   y_axix = compute_resilience(graph, attacked_order)
   plt.plot(x_axix, y_axix)
   plt.xlabel("Number of nodes removed")
   plt.ylabel("Size of the largest connect component")
   plt.title("Resilience for graphs")
   

#print attacked_order
def plot_graphs(Gs, attacked_order):
    for i in range(3):
       plot_graph(Gs[i], attacked_order[i])
       
url = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
Gs = [graphs.computer_network(url), graphs.ER(1347,0.0035), graphs.UPA(1347,5)]
legends = ["computer_network: nodes = 1347, edges = "+str(graphs.calculate_edges(Gs[0])), 
            "ER: nodes = " + str(len(Gs[1])) +" edges = "+str(graphs.calculate_edges(Gs[1]))+" p = " +str(0.0035), 
             "UPA: nodes = 1347, edges = "+str(graphs.calculate_edges(Gs[2]))+" m = " +str(5)]
attacked_orders = [pd.targeted_order(g) for g in Gs]

plot_graphs(Gs, attacked_orders)
plt.legend(legends)
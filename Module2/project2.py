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

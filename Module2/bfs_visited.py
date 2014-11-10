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
    q = deque([start_node])
    while q:
        initial_node = q.popleft()
        if initial_node in ugraph:
            if len(ugraph[initial_node]) != 0:
                neighbors = ugraph[initial_node]
                for node in neighbors:
                    if node not in visited:
                        visited.add(node)
                        q.append(node)
    return visited
    

def cc_visited(ugraph):
    """this function return connected component in graph"""
    cc = []
    unvisited = [dummy_node for dummy_node in ugraph]
    while unvisited:
        temp = set([])
        node = random.choice(unvisited)
        visited = bfs_visited(ugraph, node)
        temp = temp.union(visited)
        cc.append(temp)
        unvisited = [dummy_n for dummy_n in unvisited if dummy_n not in visited]
    return cc

def largest_cc_size(ugraph):
    """this function calculate the largest size of cc in graph"""
    cc = cc_visited(ugraph)
    if len(cc) == 0:
        return 0
    return max([len(dummy_c) for dummy_c in cc])
    
def compute_resilience(ugraph, attack_order):
    """this function measure Graph resilience"""
    sizes = [largest_cc_size(ugraph)]
    for node in attack_order:
        del ugraph[node]
        for key, values in ugraph.items():
            if node in values:
                values.remove(node)
        
        largest_size = largest_cc_size(ugraph)

        sizes.append(largest_size)        
    return sizes


EX_GRAPH2 = {0: set([1,4,5]), 1: set([2, 6]), 2: set([3,7]), 3: set([7]), 
             4: set([1]), 5: set([2]), 6: set ([]), 7: set([3]), 8: set([1,2]),
             9: set([0, 3, 4, 5, 6, 7])} #example 3
print compute_resilience(EX_GRAPH2, [0,1,2,3,4,5,6,7,8,9])
print largest_cc_size({1: set([2, 6]), 2: set([3,7]), 3: set([7]), 
             4: set([1]), 5: set([2]), 6: set ([]), 7: set([3]), 8: set([1,2]),
             9: set([3, 4, 5, 6, 7])})
print largest_cc_size({2: set([3,7]), 3: set([7]), 
             4: set([]), 5: set([2]), 6: set ([]), 7: set([3]), 8: set([2]),
             9: set([3, 4, 5, 6, 7])})
print largest_cc_size({3: set([7]), 
             4: set([]), 5: set([]), 6: set ([]), 7: set([3]), 8: set([]),
             9: set([3, 4, 5, 6, 7])})
print largest_cc_size({4: set([]), 5: set([]), 6: set ([]), 7: set([]), 8: set([]),
             9: set([4, 5, 6, 7])})
print largest_cc_size({5: set([]), 6: set ([]), 7: set([]), 8: set([]),
             9: set([5, 6, 7])})
print largest_cc_size({6: set ([]), 7: set([]), 8: set([]),
             9: set([6, 7])})
print largest_cc_size({7: set([]), 8: set([]),
             9: set([7])})
print largest_cc_size({8: set([]),
             9: set([])})
print largest_cc_size({9: set([])})
print largest_cc_size({})
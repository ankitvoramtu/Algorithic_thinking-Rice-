# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 16:18:20 2014
Project 1 - Degree distributions for graphs
For your first project, you will write Python code that creates dictionaries 
corresponding to some simple examples of graphs. You will also implement two 
short functions that compute information about the distribution of the in-degrees 
for nodes in these graphs. You will then use these functions in the Application 
component of Module 1 where you will analyze the degree distribution of a citation 
graph for a collection of physics papers. This final portion of module will be
peer assessed.
@author: zhihuixie
"""

class Graph:
    def __init__(self, num_nodes, digraph):
        self.num_nodes = num_nodes
        self.digraph = digraph
    def make_complete_graph(self): #make a complete directed graph
        g ={}
        if self.num_nodes <= 0:
            return g
        else:
            for dummy_i in range (self.num_nodes):
                g[dummy_i] = set([])
                for dummy_j in range (self.num_nodes):
                    if dummy_i != dummy_j:
                        g[dummy_i].add(dummy_j) #add an edge
            return g
    def compute_in_degrees(self):
        in_degree_g = {}
        digraph = self.digraph
        values = []
        for value in digraph.values():
            values += list(value)
        for key in digraph.keys():
            in_degree_g[key] = values.count(key) #calculate in_degree
        return in_degree_g
    def in_degree_distribution(self):
        distribution_g = {}
        G = self.compute_in_degrees()
        in_degrees = list(G.values())
        for degree in in_degrees:
            distribution_g[degree] = in_degrees.count(degree) #count number of nodes with in degree
        return distribution_g
EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])} #example 1
EX_GRAPH1 = {0: set([1,4,5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 
             4: set([1]), 5: set([2]), 6: set ([])} #example 2
EX_GRAPH2 = {0: set([1,4,5]), 1: set([2, 6]), 2: set([3,7]), 3: set([7]), 
             4: set([1]), 5: set([2]), 6: set ([]), 7: set([3]), 8: set([1,2]),
             9: set([0, 3, 4, 5, 6, 7])} #example 3

                    
        
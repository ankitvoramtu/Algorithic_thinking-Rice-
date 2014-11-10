# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 15:11:15 2014

@author: zhihuixie
"""
import pandas as pd
class Graph():
    def __init__(self, node, edge):
        self.node = node
        self.edge = edge
        self.graph = {}
    def __str__(self):
        return "The graph is: " + str(self.graph)
    def add_nodes (self):
        if self.node not in self.graph:
            self.graph[self.node] = set([])
        return self.graph
    def add_edges (self):
        self.graph[self.node] = self.graph[self.node].union(self.edge)
        return self.graph
        

df = pd.read_csv("fullbuild_MET-interactome.csv")
graph = {key: set(value) for key, value in df.groupby("Source")["Interaction"]}
#print graph
cc = []
import project2
for node in graph:
    component = project2.bfs_visited(graph, node)
    if len(component) == 2:
        print node, component
    if component not in cc:
       cc.append(project2.bfs_visited(graph, node))
print len(cc), [len(a) for a in cc]
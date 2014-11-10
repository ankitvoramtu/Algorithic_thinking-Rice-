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
"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2
import random

###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    #print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)
#print citation_graph
           
def compute_in_degrees(digraph):
    """
    This function calculates number in degrees of each node in directed graph
    """ 
    in_degree_g = {}
    values = []
    for value in digraph.values():
        values += list(value)
    for key in digraph.keys():
        in_degree_g[key] = values.count(key) #calculate in_degree
    return in_degree_g
    
def in_degree_distribution(digraph):
    """
    This function calculates number of nodes with the same degree in directed graphs
    """    
    distribution_g = {}
    in_degree_graph = compute_in_degrees(digraph)
    in_degrees = list(in_degree_graph.values())
    for degree in in_degrees:
        temp = float(in_degrees.count(degree))
        if degree != 0 and temp != 0:
           distribution_g[math.log(degree)] = math.log(temp/len(digraph)) #count number of nodes with in degree
    return distribution_g
#print in_degree_distribution(EX_GRAPH2)

def ER(num_nodes, p):
    G = {}
    for i in range(num_nodes):
        G[i] = set([])
        for j in range(num_nodes):
            if i != j:
                a = random.choice([0, 1])
                if a < p:
                    G[i].add(j)
    return G
#print ER(10, 1)
def make_complete_graph(num_nodes): 
    """
    This function build a complete directed graph with num_nodes
    """
    complete_g ={}
    if num_nodes <= 0:
        return complete_g
    else:
        for dummy_i in range (num_nodes):
            complete_g[dummy_i] = set([])
            for dummy_j in range (num_nodes):
                if dummy_i != dummy_j:
                    complete_g[dummy_i].add(dummy_j) #add an edge
        return complete_g

#from provided import DPATrial
def DPA(n, m):
    g = make_complete_graph(m)
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
#print in_degree_distribution(EX_GRAPH2)

#print DPA(10,3)
import matplotlib.pylab as pl
import math
g = in_degree_distribution (citation_graph)
#g = in_degree_distribution(DPA(27770, 13))
#g = in_degree_distribution(DPA(1000, 10))

pl.plot(list(g.keys()), list(g.values()), "ro")
#pl.xlabel("log (Number of in_degrees)")
#pl.ylabel("log (Percentage of in_degree distribution)")
#pl.title("Distributions (log/log)")
pl.xlabel("log (Number of citations)")
pl.ylabel("log (Percentage of paper with citation)")
pl.title("Distribution of citations (log/log)")
#print sum(list(g.values())), min(list(g.values())), max(list(g.values()))
#pl.plot(list(g.keys()), list(g.values()))

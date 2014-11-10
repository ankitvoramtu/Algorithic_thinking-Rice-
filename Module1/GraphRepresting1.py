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
EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])} #example 1
EX_GRAPH1 = {0: set([1,4,5]), 1: set([2, 6]), 2: set([3]), 3: set([0]), 
             4: set([1]), 5: set([2]), 6: set ([])} #example 2
EX_GRAPH2 = {0: set([1,4,5]), 1: set([2, 6]), 2: set([3,7]), 3: set([7]), 
             4: set([1]), 5: set([2]), 6: set ([]), 7: set([3]), 8: set([1,2]),
             9: set([0, 3, 4, 5, 6, 7])} #example 3
             

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
        distribution_g[degree] = in_degrees.count(degree) #count number of nodes with in degree
    return distribution_g
    


def run_trial(num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        node_numbers.append(num_nodes)
        node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        num_nodes += 1
        return new_node_neighbors


from provided import DPATrial
def DPA(n, m):
    g = make_complete_graph(m)
    for i in range(m, n):
        a = DPATrial (m)
        #print a.run_trial(m)
        value = a.run_trial(m)
        g [i] = value
    return g
#print in_degree_distribution(EX_GRAPH2)
 DPA(27770, 13)

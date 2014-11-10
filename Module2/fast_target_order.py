# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 21:17:18 2014

@author: zhihuixie
"""
import provided
import graphs
import timeit
import matplotlib.pylab as plt
def FastTargetOrder(g):
    """ return nodes by max_degree"""
    new_g = provided.copy_graph(g)
    n = len(new_g)
    degree_sets = {}
    for i in range(n):
        degree_sets[i] = set([])
    for node_d in new_g:
        degree_sets[len(new_g[node_d])].add(node_d)        
    l1 = set([])
    for j in range(n-1, -1, -1):
        #print j  
        while len(degree_sets[j]) != 0:
            node = degree_sets[j].pop()
            #degree_sets[j].remove(node)
            if node in new_g:
                neighbors = new_g[node]
            for neighbor in neighbors:
                if neighbor in new_g:
                    d = len(new_g[neighbor])
                    if neighbor in degree_sets[d]:
                        degree_sets[d].remove(neighbor)
                    if d>=1:
                        degree_sets[d-1].add(neighbor)
            if node not in l1:
                l1.add(node)
            #print l1[i]
            if node in new_g:
                del new_g[node]
 #           for dummy_key, values in new_g.items():
  #              if node in values:
   #                 values.remove(node)
    for g_node in new_g:
       l1.add(g_node)
    return l1
def timer1():
    runing_time1 = []
    #runing_time2 = []
    for n in range(10, 1000, 10):
        g = graphs.UPA(n, 5)
        start1 = timeit.default_timer()
        provided.targeted_order(g)
        stop1 = timeit.default_timer()
        runing_time1.append(stop1-start1)
        #start2 = timeit.default_timer()
        #FastTargetOrder(g)
        #stop2 = timeit.default_timer()
        #runing_time2.append(stop2-start2)
    return runing_time1#, runing_time2
def timer2():
    runing_time1 = []
    #runing_time2 = []
    for n in range(10, 1000, 10):
        g = graphs.UPA(n, 5)
        start1 = timeit.default_timer()
        FastTargetOrder(g)
        stop1 = timeit.default_timer()
        runing_time1.append(stop1-start1)
        #start2 = timeit.default_timer()
        #FastTargetOrder(g)
        #stop2 = timeit.default_timer()
        #runing_time2.append(stop2-start2)
    return runing_time1#, runing_time2
#g = graphs.ER(1347,0.0035)

"""
x_axix1 = [n for n in range(10, 1000, 10)]
y_axix1 = timer1()
y_axix2 = timer2()
plt.plot(x_axix1, y_axix1)
plt.plot(x_axix1, y_axix2)
plt.xlabel("Number of nodes")
plt.ylabel("Running time")
plt.title("Performance of function (desk_python)")
plt.legend(["Target_order", "Fast_target_order"])
"""  

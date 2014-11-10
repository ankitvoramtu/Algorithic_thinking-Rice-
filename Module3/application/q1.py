# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 19:39:14 2014

@author: zhihuixie
"""
import random
import project3
import matplotlib.pylab as plt
from alg_cluster import Cluster
import timeit
def gen_random_clusters(num_clusters):
    points = []
    for i in range(num_clusters):
        x_point = random.uniform(-1,1)
        y_point = random.uniform(-1,1)
        points.append((x_point, y_point))
    clusters = [Cluster(set([]), points[j][0], points[j][1], 0, 0) for j in range(num_clusters)]
    return clusters

def timer1():
    runing_time1 = []
    for n in range(2, 200):
        clusters = gen_random_clusters(n)
        start1 = timeit.default_timer()
        project3.slow_closest_pairs(clusters)
        stop1 = timeit.default_timer()
        runing_time1.append(stop1-start1)
    return runing_time1
def timer2():
    runing_time1 = []
    for n in range(2, 200):
        clusters = gen_random_clusters(n)
        start1 = timeit.default_timer()
        project3.fast_closest_pair(clusters)
        stop1 = timeit.default_timer()
        runing_time1.append(stop1-start1)
    return runing_time1


x_axix1 = [n for n in range(2, 200)]
y_axix1 = timer1()
y_axix2 = timer2()
plt.plot(x_axix1, y_axix1)
plt.plot(x_axix1, y_axix2)
plt.xlabel("Number of initial clusters")
plt.ylabel("Running time")
plt.title("Performance of functions (desk_python)")
plt.legend(["slow_closest_pairs", "fast_closest_pair"])


    
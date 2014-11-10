# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 21:27:52 2014

@author: zhihuixie
"""
import urllib2
import alg_cluster
import project3
import matplotlib.pylab as plt
DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]
def compute_distortion(cluster_list, data_table):
    return sum([cluster_list[i].cluster_error(data_table) for i in range (len(cluster_list))])
    

data_table = load_data_table(DATA_896_URL)
singleton_list = []
for line in data_table:
   singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
distortion_h = []
distortion_k = []
for i in range(6, 21):
    cluster_list = project3.hierarchical_clustering(singleton_list, i)
    distortion_h.append(compute_distortion(cluster_list, data_table))
    cluster_list1 = project3.kmeans_clustering(singleton_list, i, 5)
    distortion_k.append(compute_distortion(cluster_list1, data_table))
    

x_axix1 = [n for n in range(6, 21)]
y_axix1 = distortion_h
y_axix2 = distortion_k
plt.plot(x_axix1, y_axix1, marker = "o", color = "red")
plt.plot(x_axix1, y_axix2, marker = "*", color = "blue")
plt.xlabel("number of output clusters")
plt.ylabel("Distortion")
plt.title("Comparison of distortion of alg (DATA_896_URL)")
plt.legend(["hierarchical_clustering", "k-means_clustering"], loc = "upper left")

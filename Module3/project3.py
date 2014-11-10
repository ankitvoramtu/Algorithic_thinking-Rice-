# -*- coding: utf-8 -*-


"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster
from alg_cluster import Cluster


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), idx1, idx2)


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    cluster_pairs = set([]) 
    results = set([])
    distance = float("inf")
    for idx1 in range(len(cluster_list)-1):
        for idx2 in range(idx1+1, len(cluster_list)):
            (temp_distance, temp_indx_i, temp_indx_j) = pair_distance(cluster_list, idx1, idx2)
            cluster_pairs.add((temp_distance, temp_indx_i, temp_indx_j))
            if temp_distance < distance:
                distance = temp_distance
    for (dist, dindx_i, dindx_j) in cluster_pairs:
        if dist == distance:
           results.add((dist, dindx_i, dindx_j))                   
    return  results


def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """
        
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        numpoints = len(horiz_order)
        # base case
        if numpoints <= 3:
            output = slow_closest_pairs([cluster_list[horiz_order[dummy_i]] for dummy_i in range(numpoints)]).pop()
            return (output[0], horiz_order[output[1]], horiz_order[output[2]])
        # divide        
        else:
            mid = (cluster_list[horiz_order[numpoints/2 - 1]].horiz_center() + cluster_list[horiz_order[numpoints/2]].horiz_center())/2
            horiz_l = horiz_order[:numpoints/2]
            horiz_r = horiz_order[numpoints/2:]
            temp_index = [(vert_order.index(item)) for item in horiz_l]
            temp_index.sort()
            vert_l = [vert_order[dummy_i] for dummy_i in temp_index]
            temp_indexj = [(vert_order.index(item)) for item in horiz_r]
            temp_indexj.sort()
            vert_r = [vert_order[dummy_j] for dummy_j in temp_indexj]
            (dist_l, index_il, index_jl) = fast_helper(cluster_list, horiz_l, vert_l)    
            (dist_r, index_ir, index_jr) = fast_helper(cluster_list, horiz_r, vert_r)
            (dist, index_i, index_j) = (dist_r, index_ir, index_jr)
            if dist_l < dist_r:
               (dist, index_i, index_j) = (dist_l, index_il, index_jl)
        # conquer
            lists = [vert_order[i] for i in range(numpoints) if (cluster_list[vert_order[i]].horiz_center() - mid) < dist]
            num_lists = len(lists)
            for num_u in range(num_lists-1):
                for num_v in range(num_u + 1, min(num_u + 4, num_lists)):
                    (dist_s, lists[num_u], lists[num_v]) = pair_distance(cluster_list, lists[num_u], lists[num_v])
                    if dist_s < dist:
                        (dist, index_i, index_j) = (dist_s, lists[num_u], lists[num_v]) 
        return (dist, index_i, index_j)
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list 
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    num_list = len(cluster_list)
    output_clusters = []
    for dummy_i in range(num_list):
        output_clusters.append(cluster_list[dummy_i])
    while len(output_clusters) > num_clusters:
        (dummy_dist, cluster1_i, cluster2_j) = fast_closest_pair(output_clusters)
        cluster1 = output_clusters[cluster1_i]
        cluster2 = output_clusters[cluster2_j]
        merged_cluster = cluster1.merge_clusters(cluster2)
        output_clusters.append(merged_cluster)
        output_clusters.remove(cluster1)
        output_clusters.remove(cluster2)
    return output_clusters
    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function mutates cluster_list 
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    centers = []
    num_points = len(cluster_list)
    populations = [cluster_list[dummy_i].total_population() for dummy_i in range(num_points)]
    populations.sort()
    populations.reverse()
    populations = populations[:num_clusters]
    for population in populations:
        for cluster in cluster_list:
            if cluster.total_population () == population:
                centers.append(cluster)
    new_centers = list(centers)
    for dummy_index_i in range(num_iterations):
        clusters = [Cluster(set([]), cluster_list[dummy_i].horiz_center(), cluster_list[dummy_i].vert_center(), 0, 0) for dummy_i in range(num_clusters)]      
        for num_j in range(num_points):
            dist = float("inf")
            for num_f in range(num_clusters):
                dist1 = cluster_list[num_j].distance(new_centers[num_f])
                if dist1 < dist:
                    dist = dist1
                    idxn_l = num_f
            clusters[idxn_l].merge_clusters(cluster_list[num_j])        
        for num_f1 in range (num_clusters):
            new_centers[num_f1] = clusters[num_f1]           
    # initialize k-means clusters to be initial clusters with largest populations
    return clusters

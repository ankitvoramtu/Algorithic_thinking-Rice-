# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 20:22:28 2014

@author: zhihuixie
"""
import pd
import project4 as p4
import random
import matplotlib.pylab as plt
import math
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"
def local_aligment(seq_x, seq_y, scoring_matrix, aligment_matrix):
    return p4.compute_local_alignment(seq_x, seq_y, scoring_matrix, aligment_matrix)

def conserved_percentage(seq_x, seq_y, scoring_matrix, aligment_matrix):
    (score, g_alig_seq_h, g_alig_pax) = p4.compute_global_alignment(seq_x, seq_y, scoring_matrix, aligment_matrix)
    count = 0
    for index in range(len(g_alig_seq_h)):
        if g_alig_seq_h[index] == g_alig_pax[index]:
            count += 1
    return float(count)*100/len(g_alig_seq_h)

def generate_null_distribution(seq_x,seq_y, scoring_matrix, num_trials):
    scoring_distribution = {}
    for key in range(1, num_trials + 1):
        rand_seq_y = "".join(random.sample(seq_y, len(seq_y)))
        score = p4.max_compute_alignment_matrix(seq_x, rand_seq_y, scoring_matrix)
        if score in scoring_distribution:
            scoring_distribution[score] += 1
        else:
            scoring_distribution[score] = 1
    return scoring_distribution
    
seq_p_hum = pd.read_protein(HUMAN_EYELESS_URL)
seq_p_fly = pd.read_protein(FRUITFLY_EYELESS_URL)
seq_p_pax = pd.read_protein(CONSENSUS_PAX_URL)
scoring_matrix_p = pd.read_scoring_matrix(PAM50_URL)
local_aligment_matrix = p4.compute_alignment_matrix(seq_p_hum, seq_p_fly, scoring_matrix_p, False)
(score, local_alig_seq_h, local_alig_seq_f) = local_aligment(seq_p_hum, seq_p_fly, scoring_matrix_p,local_aligment_matrix)
local_alig_seq_h = local_alig_seq_h.replace("-", "")
local_alig_seq_f = local_alig_seq_f.replace("-", "")
global_aligment_matrix_h = p4.compute_alignment_matrix(local_alig_seq_h, seq_p_pax, scoring_matrix_p, True)
global_aligment_matrix_f = p4.compute_alignment_matrix(local_alig_seq_f, seq_p_pax, scoring_matrix_p, True)
#print "HUMAN_EYELESS: ", conserved_percentage (local_alig_seq_h, seq_p_pax, scoring_matrix_p,global_aligment_matrix_h)
#print "FRUITFLY_EYELESS: ", conserved_percentage (local_alig_seq_f, seq_p_pax, scoring_matrix_p,global_aligment_matrix_f)

#scor_distr = generate_null_distribution(seq_p_hum,seq_p_fly, scoring_matrix_p, 1000)
#scores = scor_distr.keys() 
#distrs = [float(value)/1000 for value in scor_distr.values()] 
#print scores, distrs
#print scor_distr
#fig = plt.figure()
#ax = plt.subplot()
#ax.bar(scores, distrs)
#plt.title("Score distribution")
#plt.xlabel("Scores")
#plt.ylabel("Fraction of total trials")
def calculate_z(scor_distr, score):
    mu = float(sum([key*value for key, value in scor_distr.items()]))/1000
    stdev = math.sqrt(float(sum([((key-mu)**2)*value for key, value in scor_distr.items()]))/1000)
    z_score = (score - mu)/stdev
    return mu, stdev, z_score
    
score = p4.max_compute_alignment_matrix(seq_p_hum,seq_p_fly, scoring_matrix_p)
scor_distr = generate_null_distribution(seq_p_hum,seq_p_fly, scoring_matrix_p, 1000)
print calculate_z(scor_distr, score)
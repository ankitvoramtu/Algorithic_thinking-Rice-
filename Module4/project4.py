# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 22:24:15 2014

@author: zhihuixie
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """This function build the scoring matrix"""
    scoring_matrix = {} #initiate an empty dict
    for item in alphabet:
        temp_dict = {}  #initiate a temp dict to store dict of each char in alphabet
        if item == "-": # dash cash
            for char in alphabet:
                temp_dict[char] = dash_score
        else:          #other cases
            for char in alphabet:
               if char == item:
                   temp_dict[char] = diag_score
               elif char == "-":
                   temp_dict[char] = dash_score
               else:
                   temp_dict[char] = off_diag_score
        scoring_matrix[item] = temp_dict
    return scoring_matrix         
def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """this function builds a matrix aligment for seq x and seq y"""
    row_l = len(seq_x) + 1
    col_l =len(seq_y) + 1
    if col_l==0 and row_l==0:
        return [[0]]
    alignment_matrix = [[0 for dummy_i in range(col_l)] for dummy_j in range(row_l)]
    if global_flag:
        for row_i in range (1, row_l): #initate scores in column
            char_x = seq_x[row_i - 1]
            alignment_matrix[row_i][0] = alignment_matrix[row_i -1] [0]+ scoring_matrix[char_x]["-"]
        for col_j in range (1, col_l): #initate scores in row
            char_y = seq_y[col_j - 1]
            alignment_matrix[0][col_j]= alignment_matrix[0][col_j -1] + scoring_matrix[char_y]["-"]
        #print alignment_matrix
    for row_i in range(1, row_l): #calculate score at position(col_i, index_j)
        char_x = seq_x[row_i - 1]
        for col_j in range(1, col_l): 
            char_y = seq_y[col_j - 1]
            score = max(alignment_matrix[row_i - 1][col_j - 1] + scoring_matrix[char_x][char_y],
                        alignment_matrix[row_i - 1][col_j] + scoring_matrix[char_x]["-"], 
                        alignment_matrix[row_i][col_j - 1] + scoring_matrix["-"][char_y])
            if global_flag:
                alignment_matrix[row_i][col_j] = score
            else:
                if score < 0:
                    score = 0
                alignment_matrix[row_i][col_j] = score
    return alignment_matrix
    
def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''Tracks back to create the aligned sequence pair'''
    seq1 = ''
    seq2 = ''
    index_x = len(seq_x)
    index_y = len(seq_y)
    while index_x > 0 and index_y > 0:
        score = alignment_matrix[index_x][index_y]
        diag_score = alignment_matrix[index_x-1][index_y-1]
        up_score =  alignment_matrix[index_x][index_y-1]
        left_score =  alignment_matrix[index_x-1][index_y]
        if score == diag_score + scoring_matrix[seq_x[index_x - 1]][seq_y[index_y - 1]]:
            seq1 = seq_x[index_x - 1] + seq1
            seq2 = seq_y[index_y - 1] + seq2
            index_x -= 1
            index_y -= 1
        elif score == left_score + scoring_matrix[seq_x[index_x - 1]]["-"]:
            seq1 = seq_x[index_x - 1] + seq1
            seq2 = '-' + seq2
            index_x -= 1
        elif score == up_score + scoring_matrix["-"][seq_y[index_y - 1]]:
            seq1 = '-' + seq1
            seq2 = seq_y[index_y - 1] + seq2
            index_y -= 1
        else:
            print'Not Possible'

    while index_x > 0:
        seq1 = seq_x[index_x - 1] + seq1
        seq2 = '-' + seq2
        index_x -= 1
 
    while index_y > 0:
        seq1 = '-' + seq1
        seq2 = seq_y[index_y - 1] + seq2
        index_y -= 1
    return (alignment_matrix[len(seq_x)][len(seq_y)], seq1, seq2)
    
def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''Tracks back to create the aligned sequence pair'''
    seq1 = ''
    seq2 = ''
    best_score = max([max(item) for item in alignment_matrix])
    end_i = 0
    end_j = 0
    for index_i in range(len(seq_x) + 1):
        for index_j in range(len(seq_y) + 1):
            if alignment_matrix[index_i][index_j] == best_score:
                (end_i, end_j) = (index_i, index_j)
    while end_i > 0 and end_j > 0:
        diag_score = alignment_matrix[end_i-1][end_j-1]
        up_score =  alignment_matrix[end_i][end_j-1]
        left_score =  alignment_matrix[end_i-1][end_j]
        if alignment_matrix[end_i][end_j] == diag_score + scoring_matrix[seq_x[end_i - 1]][seq_y[end_j - 1]]:
            seq1 = seq_x[end_i - 1] + seq1
            seq2 = seq_y[end_j - 1] + seq2
            end_i -= 1
            end_j -= 1
        elif alignment_matrix[end_i][end_j] == left_score + scoring_matrix[seq_x[end_i - 1]]["-"]:
            seq1 = seq_x[end_i - 1] + seq1
            seq2 = '-' + seq2
            end_i -= 1
        elif alignment_matrix[end_i][end_j] == up_score + scoring_matrix["-"][seq_y[end_j - 1]]:
            seq1 = '-' + seq1
            seq2 = seq_y[end_j - 1] + seq2
            end_j -= 1
        else:
            break;         
    return (best_score, seq1, seq2) 
import urllib2
import timeit
import pd
import matplotlib.pylab as plt
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
"""    
x = "a"
y = "abcd"
z = "dcad"
u = "addcdd"
while True:
    edit_dist1 = 3
    edit_dist2 = 3
    diag_score = random.choice(range(10))
    off_diag_score = random.choice(range(10))
    dash_score = random.choice([0, 1,2, 3,4,5,6,7,8,9])    
    scoring_matrix = build_scoring_matrix("abcd-", diag_score, off_diag_score, dash_score)
    score1 = compute_alignment_matrix(x, y, scoring_matrix, True)[-1][-1]
    score2 = compute_alignment_matrix(z, u, scoring_matrix, True)[-1][-1]
    if edit_dist1 == len(x) + len(y) - score1 and edit_dist2 == len(u) + len(z) - score2:
      #if diag_score == 2 and off_diag_score == 1 and dash_score == 0:
      print diag_score, off_diag_score, dash_score
      print score1, score2, len(x) + len(y) - score1, len(u) + len(z) - score2
      break;
"""
def check_spelling(checked_word, dist, word_list):
    output = []
    scoring_matrix = build_scoring_matrix("abcdefghijklmnopqrstuvwxyz-", 2, 1, 0)
    for word in word_list:
        score = compute_alignment_matrix(checked_word, word, scoring_matrix, True)[-1][-1]
        edit_dist = len(checked_word) + len(word) - score
        if edit_dist <= dist:
            output.append(word)
    return output
def read_words(filename):
    """this function read words as a set"""
    word_file = urllib2.urlopen(filename)
    words = word_file.read()
    word_list = set(word for word in words.split("\n")) #convert list to a set
    print "Total words in dictionary: ", len(word_list)
    return word_list
    
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"
word_list1 = pd.read_words(WORD_LIST_URL)
word_list2 = read_words(WORD_LIST_URL)
dist2 = 2

timer1 = []
for i in range(0, 50, 5):
    checked_words = word_list1[:i]
    start1 = timeit.default_timer()
    for checked_word in checked_words:
        check_spelling(checked_word, dist2, word_list1)
    stop1 = timeit.default_timer()
    timer1.append(stop1 - start1)
print timer1
def improved_dist(checked_word, word, distt):
    dist = 0
    checked_l = len(checked_word)
    word_l = len(word)
    if checked_word == word:
        dist = 0
    else:
        line1 = [0 for i in range(word_l + 1)]
        line2 = [0 for i in range(word_l + 1)]
        for j in range (word_l + 1):
            line1[j] = j
        for n in range (checked_l):
            line2[0] = n + 1
            for m in range (word_l):
                if checked_word[n] == word[m]:
                    cost = 0
                else:
                    cost = 1
                line2[m+1] = min(line2[m] + 1, line1[m+1] + 1, line1[m] + cost)
            for ix in range (word_l + 1):
                line1[ix] = line2[ix]
        dist = line2[-1]
    if dist > distt:
        return False
    else:
        return True
        
        
def edit_dist(checked_word, word, distt):
    l_checked = len(checked_word) + 1
    l_word = len(word) + 1
    dist = [[0 for dummy_i in range(l_word)] for dummy_j in range(l_checked)]
    for i in range (l_checked):
        dist[i][0] = i
    for j in range (l_word):
        dist[0][j] = j
    for j in range (1, l_word):
        for i in range (1, l_checked):
            if checked_word[i-1] == word[j-1]:
                dist[i][j] = dist[i -1][j-1]
            else:
                dist[i][j] = min(dist[i-1][j] + 1, dist[i][j-1] + 1, dist[i-1][j-1] + 1)
    if dist[-1][-1] > distt:
         return False
    return True
def check_words(checked_word, dist, word_list):
    output = set([])
    word_list_copy = word_list.copy()
    while word_list_copy:
        word = word_list_copy.pop()
        if abs(len(word) - len(checked_word)) <= dist:
            flag = improved_dist(checked_word, word, dist)
            if flag:
                output.add(word)
    return output
#print check_words("firefly", 2, word_list2)
    
timer2 = []
for j in range(0, 50, 5):
    checked_words2 = word_list1[:j]
    start2 = timeit.default_timer()
    for checked_word in checked_words2:
        check_words(checked_word, dist2, word_list2)
    stop2 = timeit.default_timer()
    timer2.append(stop2 - start2)
print timer2    
fig = plt.figure()
ax = plt.subplot()
ax.plot([n for n in range(0, 50, 5)], timer1, marker = "o", color = "b")
ax.plot([n for n in range(0, 50, 5)], timer2, marker = "*", color = "r")
plt.title("DP vs optimized alg")
plt.xlabel("Number of checked words")
plt.ylabel("Running time")
plt.legend(["DP", "optimized alg"], loc = 2)

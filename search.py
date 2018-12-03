import re
import time

import math
import operator

import nltk
from nltk.corpus import stopwords
from Stemmer import Stemmer

stemmer = Stemmer("english")

fields_map = { "t":0 , "p":1 , "i":2 , "e":3 , "c":4 , "r":5}

reverse_fields = { "0":"T" , "1":"P" , "2":"I" , "3":"E" , "4":"C" , "5":"R"}

map = { "t":"T" , "p":"P" , "i":"I" , "e":"E" , "c":"C" , "r":"R"}

map_weight = { "0":350.0 , "1":150.0 , "2":150.0 , "3":100.0 , "4":90.0 , "5":90.0}

N = 17000000 # Total number of documents
words = stopwords.words('english')
stopwords_dict = {}
for i in words:
    stopwords_dict[i] = 1

def process_query(q):
    global stemmer
    temp = q.split(" ")
    word_list = []
    categories = []
    for word1 in temp:
        t = word1.split(":")
        if(len(t) == 1):
            word = t[0].lower()
            try:
                stopwords_dict[word]
            except:
                s = stemmer.stemWord(word)
                word_list.append(s)
                categories.append("NA")
        else:
            word = t[1]
            cat = t[0]
            try:
                stopwords_dict[word]
            except:
                s = stemmer.stemWord(word)
                word_list.append(s)
                categories.append(cat)
    return [word_list,categories]

def binary_search(Index_lines,word,start,end):
    if(start > end):
        return "Not Found"
    mid = (start + end )/2
    temp = Index_lines[mid].split(" ")
    # print temp
    if(word > temp[0]):
        return binary_search(Index_lines,word,mid+1,end)
    elif (word < temp[0]):
        return binary_search(Index_lines,word,start,mid-1)
    else:
        return temp[1]

def find_file(word):
    Index_lines = open('highest_level_index_file').readlines()
    # print Index_lines
    while(Index_lines[0].find("InternalNode") != -1):
        line = 0
        while (line < (len(Index_lines)-1)):
            temp = Index_lines[line].split(" ")
            if(temp[0] <= word and Index_lines[line+1].split(" ")[0] > word):
                Index_lines = open(temp[1]+'.txt').readlines()
                break
            line += 1
        if(line == (len(Index_lines)-1)):
            Index_lines = open(Index_lines[line].split(" ")[1]+'.txt').readlines()
    return binary_search(Index_lines,word,0,len(Index_lines)-1)

def find_file_title(word,root):
    Index_lines = root
    while(Index_lines[0].find("InternalNode") != -1):
        line = 0
        while (line < (len(Index_lines)-1)):
            temp = Index_lines[line].split(" ")
            # print temp
            if(int(temp[0]) <= int(word) and int(Index_lines[line+1].split(" ")[0]) > int(word)):
                Index_lines = open('title'+temp[1]+'.txt').readlines()
                break
            line += 1
        if(line == (len(Index_lines)-1)):
            Index_lines = open('title'+Index_lines[line].split(" ")[1]+'.txt').readlines()
    # print Index_lines[0]
    # print 'done'
    return binary_search_title(Index_lines,word,0,len(Index_lines)-1)

def get_docID(document):
    global fields_map
    docID = ""
    flag = True
    list1 = ""
    count_list = []
    for char in document:
        if(char.isdigit() and flag == True):
            docID += char
        else:
            flag = False
        if flag == False:
            if char.isalpha():
                list1 += " " + char + " "
            else:
                list1 += char
    count_list = [0,0,0,0,0,0]
    splitList = list1.split(" ")
    splitList = splitList[1:]
    j = 0
    while(j < len(splitList)):
        count_list[fields_map[splitList[j]]] += int(splitList[j+1])
        j = j + 2
    return [docID,count_list]

def RankDocuments(query_words):
    global  N, map_weight, reverse_fields, map
    
    Rank_document = {}
    for i in range(len(query_words)):
        PL = find_file(query_words[i])
        # print PL
        if(PL != "Not Found"):
            PL = PL.split("|")
            PL[-1] = PL[-1][:-1]
            doc_freq = {}
            term_freq = 0
            for x in PL:
                temp = get_docID(x)
                doc_freq[temp[0]] = temp[1]
                term_freq += 1
            for doc in doc_freq:
                weight = 0
                for field in range(len(doc_freq[doc])):
                    if(categories[i] == "NA"):
                        weight += doc_freq[doc][field]*map_weight[str(field)] * math.log(N/(term_freq*1.0))
                    else:
                        if(map[categories[i]] == reverse_fields[str(field)]):
                            weight += doc_freq[doc][field]*map_weight[str(field)] * math.log(N/(term_freq*1.0))
                try:
                    Rank_document[doc] += weight
                except:
                    Rank_document[doc] = weight
    try:
        return Rank_document
    except:
        return -1

def binary_search_title(Index_lines,word,start,end):
    mid = (start + end )/2
    temp = Index_lines[mid].split()
    if(int(word) > int(temp[0])):
        return binary_search_title(Index_lines,word,mid+1,end)
    elif (int(word) < int(temp[0])):
        return binary_search_title(Index_lines,word,start,mid-1)
    else:
        # print ' '.join(temp[1:])
        return ' '.join(temp[1:])
        # return temp[1]

no_of_queries = input()
while(no_of_queries != 0):
    no_of_queries -= 1
    query = raw_input()
    start = time.clock()
    processedQuery = process_query(query)
    query_words = processedQuery[0]
    categories = processedQuery[1]
    Rank_document = RankDocuments(query_words)
    # print Rank_document
    if(Rank_document != -1):
        sorted_x = sorted(Rank_document.items(), key=operator.itemgetter(1),reverse = True)
        if(len(sorted_x) == 0):
            print "No documents found"
        else:
			print "\nThe list of documents title found: "
			# count = 0
			title_set = {}
			for i in range(len(sorted_x)):
				# count += 1
				if(len(title_set) == 10):
					break
				docID = sorted_x[i][0]
				final_index_title = open('highest_level_index_file_title').readlines()
				title = find_file_title(docID,final_index_title)
				if len(title_set) == 0:
					title_set = {title}
				title_set.add(title)
				# print title
			for i in title_set:
				print i
    else:
        print "No documents found"
    print

elapsed = (time.clock() - start)
print "Time %.2gs" %elapsed

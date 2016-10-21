#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html


"""
The simple implementation of Sentence2Vec using Word2Vec.
"""

import csv
import os
import math

def getCsv(csv_path):
    newdict = {}
    with open(csv_path, 'r') as csvfile:
        filereader = csv.reader(csvfile, delimiter=' ')
        for line in filereader:
            newvalues = [float(x) for x in line[1:]]
            newdict[line[0]] = newvalues
    return newdict

def compare(input_file_id, dataset_dict, input_dict):
    input_file_vec = input_dict[input_file_id]
    results = []
    
    for key in dataset_dict:
        results.append((cosine_distance(input_file_vec, dataset_dict[key]), key))
    
    return sorted(results)

    
# copied from Assg1, may not be correct
def cosine_distance(vector_1, vector_2):
    dot_1_1 = dot_product(vector_1, vector_1)
    dot_2_2 = dot_product(vector_2, vector_2)
    dot_1_2 = dot_product(vector_1, vector_2)
    if not dot_1_1 == 0 and not dot_2_2 == 0:
        len1 = math.sqrt(dot_1_1)
        len2 = math.sqrt(dot_2_2)
        return dot_1_2 / (len1 * len2)
    else:
        return 0.0

def dot_product(vector_1, vector_2):
    return sum(map(lambda x: x[0] * x[1], zip(vector_1, vector_2)))

if __name__ == '__main__':
    dataset_csv_path = 'vine-desc-training-results.txt'
    input_csv_path = 'vine-desc-validation-results.txt'
    
    dataset_dict = getCsv(dataset_csv_path)
    input_dict = getCsv(input_csv_path)
    
    temp_array = compare("1000861821491707904", dataset_dict, input_dict)
    
    for score, file_id in temp_array:
        print(file_id, ": ", score)
    
    
    

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

class CompareTextual:

    def __init__(self, dataset_csv_path, input_csv_path, classification_path):
        self.dataset_dict = self.getCsv(dataset_csv_path)
        self.input_dict = self.getCsv(input_csv_path)
        self.classi_dict = self.get_dataset_classification(classification_path)

    def getCsv(self, csv_path):
        newdict = {}
        with open(csv_path, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ')
            for line in filereader:
                newvalues = [float(x) for x in line[1:]]
                newdict[line[0]] = newvalues
        return newdict

    def get_dataset_classification(self, file_path):
        newdict = {}
        with open(file_path, 'r') as classi_file:
            filereader = csv.reader(classi_file, delimiter='\t')
            for line in filereader:
                newdict[line[0]] = int(line[1])
        return newdict

    # main method to use to get category
    def get_category(self, input_file_id, num_results):
        results_dict = self.get_category_dict(input_file_id, num_results)

        results_list = []
        for key in results_dict:
            results_list.append((key, results_dict[key]))

        return sorted(results_list, key=lambda x: x[1], reverse=True)

    # extracted method to easily run automated testing of results
    def get_category_dict(self, input_file_id, num_results):
        results = self.compare(input_file_id, num_results)
        results_dict = {}

        for i in range(1, 31):
            results_dict[i] = 0.0

        for weight, file_id in results:
            results_dict[self.classi_dict[file_id]] += 1.0

        for key in results_dict:
            results_dict[key] /= num_results

        return results_dict

    def automated_queries(self, input_classification_path):
        newdict = {}
        with open(input_classification_path, 'r') as classi_file:
            filereader = csv.reader(classi_file, delimiter='\t')
            for line in filereader:
                newdict[line[0]] = int(line[1])

        totalf1score = 0.0
        num_queries = 0
        for key in newdict:
            results_dict = self.get_category_dict(key, 100)
            precision = results_dict[newdict[key]]
            recall = results_dict[newdict[key]] # since 100 is also the number of relevant results
            if precision < 0.0005:
                f1score = 0.0
            else:
                f1score = (2 * precision * recall) / (precision + recall)
            totalf1score += f1score
            num_queries += 1
            if num_queries % 10 == 0:
                print("Processed ", num_queries, " queries, total score: ", totalf1score)

        averagef1score = totalf1score / num_queries

        print ("Average f1: ", averagef1score)



    def compare(self, input_file_id, num_results):
        input_file_vec = self.input_dict[input_file_id]
        results = []

        for key in self.dataset_dict:
            results.append((self.cosine_distance(input_file_vec, self.dataset_dict[key]), key))

        return sorted(results)[-num_results:]

    def cosine_distance(self, vector_1, vector_2):
        dot_1_1 = self.dot_product(vector_1, vector_1)
        dot_2_2 = self.dot_product(vector_2, vector_2)
        dot_1_2 = self.dot_product(vector_1, vector_2)
        if not dot_1_1 == 0 and not dot_2_2 == 0:
            len1 = math.sqrt(dot_1_1)
            len2 = math.sqrt(dot_2_2)
            return dot_1_2 / (len1 * len2)
        else:
            return 0.0

    def dot_product(self, vector_1, vector_2):
        return sum(map(lambda x: x[0] * x[1], zip(vector_1, vector_2)))

if __name__ == '__main__':
    dataset_csv_path = 'vine-desc-training-results.txt'
    input_csv_path = 'vine-desc-validation-results.txt'
    classification_path = 'vine-venue-training.txt'
    input_classification_path = 'vine-venue-validation.txt'

    comparator = CompareTextual(dataset_csv_path, input_csv_path, classification_path)

    comparator.automated_queries(input_classification_path)

    """
    result_list = comparator.get_category("1000861821491707904", 100)

    for file_id, weight in result_list:
        print(file_id, ": ", weight)
    """

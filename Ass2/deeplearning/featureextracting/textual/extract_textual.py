#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html


"""
The simple implementation of Sentence2Vec using Word2Vec.
"""

import logging
import sys
import os
from word2vec import Word2Vec, Sent2Vec, LineSentence

def sortText(in_path, out_path):
    ofile = open(out_path, 'w', encoding="mbcs")
    
    text_dict = {}
    
    with open(in_path, 'r', encoding="mbcs") as file:
        for line in file:
            file_name = line.split("\t")[0]
            text_dict[file_name] = line
    
    for key in sorted(text_dict):
        ofile.write(text_dict[key])
    
    ofile.close()

def getTextualFeature(text_reading_path):
    # Train and save the Word2Vec model for the text file.
    # Please note that, you can change the dimension of the resulting feature vector by modifying the value of 'size'.
    model = Word2Vec(LineSentence(text_reading_path), size=500, window=5, sg=0, min_count=5, workers=8)
    model.save(text_reading_path + '.model')

    # Train and save the Sentence2Vec model for the sentence file.
    model = Sent2Vec(LineSentence(text_reading_path), model_file=text_reading_path + '.model')
    model.save_sent2vec_format(text_reading_path + '.vec')

    program = os.path.basename(sys.argv[0])



if __name__ == '__main__':
    dataset_text_path = 'vine-desc-training.txt'
    input_text_path = 'vine-desc-validation.txt'
    
    dataset_text_sorted_path = 'vine-desc-training-sort.txt'
    input_text_sorted_path = 'vine-desc-validation-sort.txt'
    
    combined_text_path = 'vine-desc.txt'
    
    dataset_csv_path = 'vine-desc-training-results.txt'
    input_csv_path = 'vine-desc-validation-results.txt'
    
    # sort the text from both files
    sortText(dataset_text_path, dataset_text_sorted_path)
    sortText(input_text_path, input_text_sorted_path)
    
    # combine the sorted text, and keeps track of the file ids
    # NOTE: ASSUMES EXTRA BLANK LINE FOR DATASET TEXT FILE
    num_lines_dataset = 0
    dataset_file_ids = []
    input_file_ids = []
    with open(combined_text_path, 'w', encoding="mbcs") as ct_file:
        with open(dataset_text_sorted_path, 'r', encoding="mbcs") as ds_file:
            for line in ds_file:
                ct_file.write(line)
                dataset_file_ids.append(line.split("\t")[0])
                num_lines_dataset += 1
        with open(input_text_sorted_path, 'r', encoding="mbcs") as in_file:
            for line in in_file:
                ct_file.write(line)
                input_file_ids.append(line.split("\t")[0])
    
    # get vectors for combined text
    getTextualFeature(text_reading_path=combined_text_path)
    
    # split vectors into dataset and input
    num_dataset_lines_read = 0
    num_input_lines_read = 0
    num_data_lines = 0
    first_line = True
    with open(combined_text_path + '.vec', 'r') as vec_file:
        with open(dataset_csv_path, 'w') as dsc_file:
            with open(input_csv_path, 'w') as inc_file:
                for line in vec_file:
                    if first_line:
                        num_data_lines = line.split(" ")[0]
                        first_line = False
                        continue
                    values = line.partition(" ")[2]
                    if num_dataset_lines_read < num_lines_dataset:
                        new_line = dataset_file_ids[num_dataset_lines_read] + " " + values
                        dsc_file.write(new_line)
                        num_dataset_lines_read += 1
                    else:
                        new_line = input_file_ids[num_input_lines_read] + " " + values
                        inc_file.write(new_line)
                        num_input_lines_read += 1
                    if num_dataset_lines_read + num_input_lines_read == num_data_lines:
                        break

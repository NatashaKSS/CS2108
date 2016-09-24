# import the necessary packages
from pyimagesearch.querylogic import QueryLogic
import argparse
import csv
import os

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=False, default='queries',
                help="Path to the directory that contains the images to be \
                queried")
ap.add_argument("-r", "--result", required=False, default='result.csv',
                help="Path to where the computed results will be stored")
ap.add_argument("-i", "--index", required=False, default='pathindex_train.csv',
                help="Path to the file where the indices of files are stored")
args = vars(ap.parse_args())

querylogic = QueryLogic()

with open(args["index"]) as f:
    # initialize the CSV reader
    reader = csv.reader(f)
    file_index = {}
    for row in reader:
        key = row[0]
        value = [str(x) for x in row[1:]]
        file_index[key] = value;

first_directories = os.listdir(args["dataset"])

num_per_category = 50 # for training dataset
EPS = 1e-9

with open(args["result"], "w") as f2:
    for first_directory in first_directories:
        directory = os.path.join(args["dataset"], first_directory)
        if os.path.isdir(directory):
            files = os.listdir(directory)
            for file in files:
                filepath = os.path.join(directory, file)
                print "Processing " + filepath + "\n"
                num_match = 0
                num_result = 0
                image_attrs = querylogic.get_image_attrs(filepath)
                results = querylogic.get_search_results(image_attrs)
                for (score, result) in results:
                    if result in file_index[first_directory]:
                        num_match += 1
                    num_result += 1
                pscore = num_match / float(num_result)
                rscore = num_match / float(num_per_category)
                mapscore = 2 * pscore * rscore / (pscore + rscore + EPS)
                f2.write("%s,%d,%f,%f" % (file, num_match, pscore, mapscore))
                for (score, result) in results:
                    f2.write("," + result)
                f2.write("\n")

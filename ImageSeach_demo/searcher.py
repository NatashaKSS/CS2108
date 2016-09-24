# import the necessary packages
import numpy as np
import math
import csv
import cv2
from itertools import izip

class Searcher:

    def __init__(self, indexPath):
        # store our index path
        self.indexPath = indexPath

    def search(self, queryFeatures, limit=16):
        # initialize our dictionary of results
        results = {}

        # open the index file for reading
        with open(self.indexPath) as f:
            # initialize the CSV reader
            reader = csv.reader(f)

            # loop over the rows in the index
            for row in reader:
                # parse out the image ID and features, then compute the
                # chi-squared distance between the features in our index
                # and our query features
                features = [float(x) for x in row[1:]]
                #d = self.chi2_distance(features, queryFeatures)
                d = self.cosine_distance(features, queryFeatures)

                # now that we have the distance between the two feature
                # vectors, we can udpate the results dictionary -- the
                # key is the current image ID in the index and the
                # value is the distance we just computed, representing
                # how 'similar' the image in the index is to our query
                results[row[0]] = d

            # close the reader
            f.close()

        return results.items()

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
        return sum(map(lambda x: x[0] * x[1], izip(vector_1, vector_2)))

    def chi2_distance(self, histA, histB, eps=1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                          for (a, b) in zip(histA, histB)])

        # return the chi-squared distance
        return d

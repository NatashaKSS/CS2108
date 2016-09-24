import os, sys, math, numpy, getopt, re, pickle, csv
from itertools import izip

#======================================================================#
# Program Description:
# Searches for all relevant imgIDs with reference to the query image's
# visual concept feature vector.
#======================================================================#

def execute_vis_concept(query_img_file_path, img_vectors):
    query_img_file_vis_concept_vector_path = query_img_file_path[:-4] + ".txt"
    query_img_vector = \
        load_visual_concept_query_img_vectors(query_img_file_vis_concept_vector_path)

    #result_euclid = []
    result_cosine = []
    for imgID in img_vectors.keys():
        #result_euclid.append((imgID, euclidean_distance(query_img_vector, img_vectors[imgID])))
        result_cosine.append((imgID, cosine_distance(query_img_vector, img_vectors[imgID])))

    # For debugging
    # sorted_scores_eu = sorted(result_euclid, key = lambda x: x[1], reverse=False)
    # sorted_scores_eu = sorted_scores_eu[:25]

    # For debugging
    # Largest cosine similarity is the best
    # sorted_scores_cos = sorted(result_cosine, key = lambda x: x[1], reverse=True)
    # sorted_scores_cos = sorted_scores_cos[:10]

    return result_cosine

"""
# Note that euclidean distance is botched, don't use it
def euclidean_distance(vector_1, vector_2):
    dist = [(a - b) ** 2 for a, b in zip(vector_1, vector_2)]
    dist = math.sqrt(sum(dist))
    return dist
"""

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
    return sum(map(lambda x: x[0] * x[1], izip(vector_1, vector_2)))

#======================================================================#
# Loading necessary visual concept vectors
#======================================================================#
def load_visual_concept_img_vectors(vis_concept_path):
    from_vis_concept_index = open(vis_concept_path, "r")
    img_vectors_list = pickle.load(from_vis_concept_index)
    return img_vectors_list

def load_visual_concept_query_img_vectors(vis_concept_path):
    concept_vector = []
    with open(vis_concept_path, "r") as from_query_img_text_tag_file:
        # Process the concept_vector. Remove the last element as it is spoilt.
        concept_vector =  from_query_img_text_tag_file.readline().split(" ")[:-1]
        i = 0
        for val in concept_vector:
            concept_vector[i] = float(val)
            if float(val) < 0:
                concept_vector[i] = 0
            i = i + 1
        from_query_img_text_tag_file.close()
    return concept_vector

#======================================================================#
# Interpretation of program arguments
#======================================================================#
def usage():
    """
    'How-to-use' message in case user does not follow program input format
    """
    print "usage: " + sys.argv[0] + " -q path-to-query-img"

# Initialize required variables to store file paths
query_img_file_path = None

# Save file path arguments into their respective variables
try:
    opts, args = getopt.getopt(sys.argv[1:], 'q:')
except getopt.GetoptError, err:
    # Throw error in case user does not follow program input option format
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-q':
        query_img_file_path = a
    else:
        assert False, "unhandled option"
if query_img_file_path == None:
    print "Did you miss out any options?"
    print
    usage()
    sys.exit(2)

#=====================================================#
# Execution of Program
#=====================================================#

# Train set
# img_vectors = load_visual_concept_img_vectors("semanticpickle.txt")

# Test set
img_vectors = load_visual_concept_img_vectors("semantictestpickle.txt")

execute_vis_concept(query_img_file_path, img_vectors)

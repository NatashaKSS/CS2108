import os
import sys
import glob
import getopt
import re
import pickle
import csv

#======================================================================#
# Program Description:
# Searches for all relevant imgIDs with reference to the query image's
# text tag search query.
#
# The result of the query will be written to the specified output file,
# containing all relevant imgIDs.
#
# Execute this program like this:
# .\compute_search_score_of_text_tags.py
# -q ./queries\0594_2309034355.jpg -n 0594_2309034355
# -p testset_text_tags_postings.txt
# -c .\semantic_feature_1000_classifications.csv
# -s .\semantic_feature_extractor_file_names.txt
#
# The path for the image query file is set after the -q flag.
# The path for the postings file specified after the -p  flag should be the
# postings file produced when you indexed the training data's text_tags.
#======================================================================#
def execute():
    print process_query(get_query_visual_concept_text_tag())

def compute_similarity():
    scores = {}

def process_query(q):
    processed_q = re.split('\W+', q)
    processed_q = [term.lower() for term in processed_q if not term in stop_words\
                   and not term in excluded_chars]
    return processed_q

#======================================================================#
# Load necessary files
#======================================================================#
def load_postings():
    from_postings_file = open(postings_file, "r")
    return pickle.load(from_postings_file)

def load_visual_concept_classes():
    with open(classifications_file, 'rb') as file:
        reader = csv.reader(file)
        query_classifications = list(reader)
    file.close()
    return query_classifications

def get_query_visual_concept_text_tag():
    # Represents the image ID's text tag's file name
    query_img_text_tag_file_path = query_img_file_path[:-4] + ".txt"

    # Auxiliary variable to accumulate visual concept classes of this query img
    vc_classes_retrieved = []

    if (os.path.isfile(query_img_text_tag_file_path)):
        with open(query_img_text_tag_file_path, "r") as from_query_img_text_tag_file:
            # Process the concept_vector. I found that the last element was spoilt.
            concept_vector =  from_query_img_text_tag_file.readline().split(" ")[:-1]
            # List of indexes of text_tags that correspond to the 1000classification file
            text_tags_index_list = []

            for index, val in enumerate(concept_vector):
                if float(val) > 0:
                    # Values > 0 mean that this img is highly related to the concept
                    text_tags_index_list.append((index, float(val)))

            # Sort the text_tags according to their concept relevance
            text_tags_index_sorted_list = \
                sorted(text_tags_index_list, key = lambda x: -x[1])

            # Get the corresponding visual classifications description for the
            # query image's text_tags index
            i = 0
            max_top_ranks = 5
            vc_classes_retrieved = ""
            for index in text_tags_index_sorted_list:
                if i < 5:
                    vc_classes_retrieved += visual_concept_classes[index[0]][0]
                    i = i + 1
        from_query_img_text_tag_file.close()
    else:
        print "Did you input the correct query img file path?"

    return vc_classes_retrieved

#======================================================================#
# Interpretation of program arguments
#======================================================================#
def usage():
    """
    'How-to-use' message in case user does not follow program input format
    """
    print "usage: " + sys.argv[0] + " -q path-to-query-img -n name-of-img " +\
    "-p postings-file -c classifications-file -s semantic_feature_results"

# Initialize required variables to store file paths
query_img_file_path = query_img_name = postings_file = classifications_file = \
semantic_results_files= None

# Save file path arguments into their respective variables
try:
    opts, args = getopt.getopt(sys.argv[1:], 'q:n:p:c:s:')
except getopt.GetoptError, err:
    # Throw error in case user does not follow program input option format
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-q':
        query_img_file_path = a
    elif o == '-n':
        query_img_name = a
    elif o == '-p':
        postings_file = a
    elif o == '-c':
        classifications_file = a
    elif o == '-s':
        semantic_results_files = a
    else:
        assert False, "unhandled option"
if query_img_file_path == None or query_img_name == None or classifications_file == None or \
    semantic_results_files == None or postings_file == None:
    print "Did you miss out any options?"
    print
    usage()
    sys.exit(2)

#=====================================================#
# Execution of Program
#=====================================================#

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', \
'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', \
'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they',\
'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',\
'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',\
'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',\
'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',\
'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against',\
'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',\
'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',\
'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',\
'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',\
'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',\
'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

excluded_chars = ['']

# Load query classification table for each semantic visual concept
visual_concept_classes = load_visual_concept_classes()

# Load postings before processing search queries
term_imgID_map = load_postings()

# Load semantic feature computation for query image
query_vis_concept_text_tag = get_query_visual_concept_text_tag()

# execute
execute()

import sys
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
# python .\compute_search_score_of_text_tags.py -q ../ImageData/test/1234.jpg
# -p testset_text_tags_postings.txt
#
# The path for the image query file is set after the -q flag.
# The path for the postings file specified after the -p  flag should be the
# postings file produced when you indexed the training data's text_tags.
#======================================================================#

def compute_similarity():
    scores = {}


def load_postings():
    from_postings_file = open(postings_file, "r")
    return pickle.load(from_postings_file)

def load_query_text_semantic_feature():
    with open('semantic_feature_1000_classifications.csv', 'rb') as file:
        reader = csv.reader(file)
        query_classifications = list(reader)
    file.close()
    return query_classifications

#======================================================================#
# Interpretation of program arguments
#======================================================================#
def usage():
    """
    'How-to-use' message in case user does not follow program input format
    """
    print "usage: " + sys.argv[0] + " -q path-to-query-img -p postings-file"

# Initialize required variables to store paths to resources on disk
query_img_file = postings_file = None

# Save arguments into their respective variables
try:
    opts, args = getopt.getopt(sys.argv[1:], 'q:p:')
except getopt.GetoptError, err:
    # Throw error in case user does not follow program input option format
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-q':
        query_img_file = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"
if query_img_file == None or postings_file == None:
    usage()
    sys.exit(2)

#=====================================================#
# Execution of Program
#=====================================================#

# Load query classification table for each semantic visual concept
query_classifications = load_query_text_semantic_feature()
print query_classifications

# Load postings before processing search queries
term_imgID_map = load_postings()

import sys
import getopt
import pickle
import tokenize
from os import listdir

#======================================================================#
# Program Description:
# Indexes image tags into a term frequency inverted index structure.
# The term_imgID_map will be stored in a postings list are on the disk in
# according to the specified file path. A postings file is a mapping of
# term to imgIDs that contain this term. This facilitates the computation of
# the similarity scores in the search phase.
#
# Execute this indexer like this:
# python .\index_text_tags.py -i ../ImageData/test/test_text_tags.txt
# -d testset_text_tags_dict.txt -p testset_text_tags_postings.txt
#
# This example indexes text tags from the test set for simplicity but you can
# do it for the training set too. The output files specified after the -d and
# -p  flags can be renamed by you, this is only an example. The file path
# after the -i flag must be a valid file path.
#======================================================================#

def construct_inverted_index():
    """
    Constructs the inverted index in-memory before writing to disk.

    Note: The contents of the text tags are in the format <imgID> <text tags>
    """
    file_text = open(path_to_text_tags, "r").read()
    lines = file_text.split("\n")

    tokens = imgID = text_tag_tokens = None
    for line in lines:
        tokens = line.split(" ")
        imgID = tokens[0]

        # 1st element is imgID, so process remaining tokens
        text_tag_tokens = process_text_tag_tokens(tokens[1:])

        # Add each term to term_imgID_map and assign it the imgIDs it
        # appears in
        for term in text_tag_tokens:
            if not term_imgID_map.has_key(term):
                term_imgID_map[term] = []
            term_imgID_map[term].append(imgID)

    # Write to to_postings_file
    # Note: pickles are an easy way to store Python objects in text files so
    # that another python program can load it straightaway, without any
    # convoluted method for reading line by line!
    to_postings_file = open(postings_file, "w")
    pickle.dump(term_imgID_map, to_postings_file)
    to_postings_file.close()

def process_text_tag_tokens(tokens):
    """
    Pre-processing step to get text tag tokens from each line. Ensures no
    duplicate tokens are found and removes empty strings in the list.
    """
    text_tag_tokens = filter(None, tokens) # remove empty strings
    text_tag_tokens = set(text_tag_tokens) # remove duplicate tokens
    return text_tag_tokens

#======================================================================#
# Interpretation of program arguments
#======================================================================#
def usage():
    """
    'How-to-use' message in case user does not follow program input format
    """
    print "usage: " + sys.argv[0] + " -i path-to-text-tags" \
    " -p postings-file"

# Initialize required variables to store paths to resources on disk
path_to_text_tags = postings_file = None

# Save arguments into their respective variables
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:p:')
except getopt.GetoptError, err:
    # Throw error in case user does not follow program input option format
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        path_to_text_tags = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"
if path_to_text_tags == None or postings_file == None:
    usage()
    sys.exit(2)

#=====================================================#
# Execution of Program
#=====================================================#

# Initialize mappings for term and imgIDs each term appears in
# Mapping in the form of:
# { term : [docFreq, value of pointer offset in postings file] }
term_imgID_map = {}

# Point of indexing execution
construct_inverted_index()

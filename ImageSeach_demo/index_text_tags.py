import sys, getopt, pickle, csv
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
# -p testset_text_tags_postings.txt
#
# This example indexes text tags from the test set for simplicity but you can
# do it for the training set too. The output files specified after the -d and
# -p  flags can be renamed by you, this is only an example. The file path
# after the -i flag must be a valid file path.
#======================================================================#

def construct_inverted_index(path_to_text_tags, postings_file_path):
    """
    Constructs the inverted index in-memory before writing to disk. Writes to the
    postings file specified.

    Note: The contents of the text tags are in the format <imgID> <text tags>
    """
    file_text = open(path_to_text_tags, "r").read()
    lines = file_text.split("\n")[:-1] # Remove last line because it is empty

    # Initialize mappings for term and imgIDs each term appears in
    # Mapping in the form of:
    # { term : [ <docFreq>, <list of imgIDs this term was found in> ] }
    term_imgID_map = {}

    # Auxiliary data to be used in search
    list_of_imgID = []
    imgID_len_map = {}

    tokens = imgID = text_tag_tokens = None
    for line in lines:
        tokens = line.split(" ")

        # The imgID is the exact path of that image
        imgID = generate_image_file_path(tokens[0])
        # 1st element is imgID, so process remaining tokens
        text_tag_tokens = process_text_tag_tokens(tokens[1:])
        # Accumulate list of imgIDs for search later
        list_of_imgID.append(imgID)
        # Accumulate list of lens of imgs for search later
        imgID_len_map[imgID] = len(text_tag_tokens)

        # Add each term to term_imgID_map and assign it the imgIDs it appears in
        for term in text_tag_tokens:
            if not term_imgID_map.has_key(term):
                term_imgID_map[term] = []
            term_imgID_map[term].append(imgID)

    # Write to to_postings_file
    to_postings_file = open(postings_file, "w")
    pickle.dump(term_imgID_map, to_postings_file)
    pickle.dump(list_of_imgID, to_postings_file)
    pickle.dump(imgID_len_map, to_postings_file)
    to_postings_file.close()

def process_text_tag_tokens(tokens):
    """
    Pre-processing step to get text tag tokens from each line. Ensures no
    duplicate tokens are found and removes empty strings in the list.
    """
    text_tag_tokens = filter(None, tokens) # remove empty strings
    text_tag_tokens = set(text_tag_tokens) # remove duplicate tokens
    return text_tag_tokens

def load_index_to_image_file_paths():
    img_file_paths = []
    with open(path_to_image_index, 'rb') as file:
        reader = csv.reader(file)
        img_file_paths = list(reader)
        file.close()
    return img_file_paths

def generate_image_file_path(img_ID):
    # Remove "pathindex_train" in front and ".csv" at the back
    train_or_test = path_to_image_index[10:-4]

    # Get category text for this particulat img_ID
    category_dir = ""
    for category_img_id_list in index_to_img_file_paths:
        if img_ID in category_img_id_list:
            category_dir = category_img_id_list[0]

    # The full path is like ../ImageData/train/data/alley/0028_1070815604.jpg
    dir = "../ImageData/" + train_or_test + "/data/" + category_dir + "/" + img_ID

    return dir

#======================================================================#
# Interpretation of program arguments
#======================================================================#
def usage():
    """
    'How-to-use' message in case user does not follow program input format
    """
    print "usage: " + sys.argv[0] + "-d path-to-image-index -i path-to-text-tags \
          -p postings-file"
    print "Please ensure that pathindex_train.csv or pathindex_test.csv names \
          ARE UNCHANGED"

# Initialize required variables to store paths to resources on disk
path_to_image_index = path_to_text_tags = postings_file = None

# Save arguments into their respective variables
try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:i:p:')
except getopt.GetoptError, err:
    # Throw error in case user does not follow program input option format
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-d':
        path_to_image_index = a
    elif o == '-i':
        path_to_text_tags = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"
if path_to_image_index == None or path_to_text_tags == None or postings_file == None:
    usage()
    sys.exit(2)

#=====================================================#
# Execution of Program
#=====================================================#
# Load the index to image file paths
index_to_img_file_paths = load_index_to_image_file_paths()

# Point of indexing execution
construct_inverted_index(path_to_text_tags, postings_file)

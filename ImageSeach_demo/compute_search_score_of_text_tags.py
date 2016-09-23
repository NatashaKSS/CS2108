import os, sys, math, glob, getopt, re, pickle, csv

#======================================================================#
# Program Description:
# Searches for all relevant imgIDs with reference to the query image's
# text tag search query.
#
# The result of the query will be written to the specified output file,
# containing all relevant imgIDs.
#
# Execute this program like this:
# ./compute_search_score_of_text_tags.py -q ./queries/0026_255236107.jpg
# -p testset_text_tags_postings.txt -c ./semantic_feature_1000_classifications.csv
# -s ./semantic_feature_extractor_file_names.txt
#
# The path for the image query file is set after the -q flag.
# The path for the postings file specified after the -p  flag should be the
# postings file produced when you indexed the training data's text_tags.
#======================================================================#

# TODO: HEY NATASHA REMEMBER TO SPECIFY THE IMG PATH HERE IN EXECUTE FUNCTION
# AS IT IS THE POINT OF ENTRY OF THE TEXT RETRIEVAL ENGINE
def execute(term_imgID_map_and_list_of_imgIDs, with_vis_concept, query_string = None):
    """
    Main execution point of text retrieval engine

    return    ranked list of top 16 search results. The returned list is of
              the format [(img path, tf-idf score), (...,...), ...].
              If no ranked list is found, an empty list is returned (this can
              occur if the visual concept detector does not return any text_tag,
              or the result images themselves have no text tags).
    """
    # Load semantic feature computation for query image and normalize query terms
    if with_vis_concept:
        query_string = get_query_visual_concept_text_tag(query_img_file_path)

    # Empty query strings will not be processed
    normalized_query_list = []
    if not query_string == None:
        normalized_query_list = process_query(query_string)

    # Get term freq mapping for query terms
    query_term_freq_map = compute_query_term_freq_weights(normalized_query_list)

    # print "normalized query list: ", normalized_query_list
    print get_top_results(set(normalized_query_list), query_term_freq_map,
                          term_imgID_map_and_list_of_imgIDs[0],
                          term_imgID_map_and_list_of_imgIDs[1],
                          term_imgID_map_and_list_of_imgIDs[2])

def process_query(q):
    """
    Pre-process the query string:
    Split on every non-word string, lowercase it, remove stop words and
    any other chars that we deem need to be excluded

    q   List of String query terms
    return  normalized list of String query terms (may contain duplicates)
    """
    processed_q = re.split('\W+', q)
    processed_q = [term.lower() for term in processed_q\
                   if not term in stop_words and not term in excluded_chars]
    return processed_q

#======================================================================#
# Compute tf-idf
#======================================================================#
def get_top_results(list_of_query_terms, query_term_freq_map, \
                    term_postings, list_of_imgIDs, imgID_len_map):
    """
    Searches for the top 16 ranking results for the specified queries.

    list_of_query_terms    List of query terms which are normalized and
                           have no duplicates.
    query_term_freq_map    A mapping of log term frequency weights for each
                           query term.
    term_postings          Postings list of all terms
    return    List of top 16 results. The scores are sorted in descending
              order and imgIDs are sorted in ascending order during a
              tie-breaker.
    """
    scores = {}
    list_of_query_idf = []

    for query_term in list_of_query_terms:
        all_postings_terms = term_postings.keys()

        # Term will be ignored if it does not exist in the dictionary
        if query_term in all_postings_terms:
            query_term_freq_weight = query_term_freq_map[query_term]
            query_term_idf = get_idf(term_postings[query_term], \
                                     len(list_of_imgIDs))

            # Accumulate list of query idf values for computation of normalized query length
            list_of_query_idf.append(query_term_idf)
            query_term_weight = query_term_freq_weight * query_term_idf

            # Dot product of query vector and doc vectors
            for curr_imgID in term_postings[query_term]:
                doc_term_weight = get_log_term_freq_weighting(query_term_freq_weight)

                # Dot product of query and doc term weights
                if not scores.has_key(curr_imgID):
                    scores[curr_imgID] = 0
                scores[curr_imgID] += query_term_weight * doc_term_weight

    # Normalization of query and iimgID vectors so that comparison is fair
    query_norm = get_query_unit_magnitude(list_of_query_idf)
    for imgID in scores.keys():
        norm_magnitude = query_norm * math.sqrt(imgID_len_map[imgID])
        scores[imgID] = scores[imgID] / norm_magnitude

    # Ranks the scores in descending order
    ranked_scores = sorted(scores.items(), \
                    key = lambda score_pair: score_pair[1], reverse = True)[:16]
    return ranked_scores

def get_idf(term_postings, N):
    """
    Computes the idf of a query term.

    term_postings    postings of a query term
    N                Total number of documents in corpus.
    return           Inverse doc frequency of a query term.
    """
    doc_freq = len(term_postings)
    if doc_freq == 0:
        # query term does not occur in ANY document so it has no weight
        return 0
    else:
        return math.log(N / doc_freq, 10)

def compute_query_term_freq_weights(normalized_query_list):
    """
    Computes the term frequency log weights of each query term in the input.
    Will compute duplicated query terms only once.

    normalized_query_list    List of query terms which have been case-folded.
                             Duplicate query terms are not filtered.
    return    A mapping of term frequencies for each query term
    """
    query_term_freq_map = {}
    for query_term in normalized_query_list:
        if not query_term_freq_map.has_key(query_term):
            query_term_freq_map[query_term] = \
                get_log_term_freq_weighting(normalized_query_list.count(query_term))
    return query_term_freq_map

def get_log_term_freq_weighting(term_freq):
    """
    Computes the logarithmic frequency weight of a term

    term_freq    Term frequency in a document.
    return       Log term frequency weight.
    """
    if term_freq == 0:
        return 0;
    else:
        return 1 + math.log(term_freq, 10)

def get_query_unit_magnitude(list_of_query_idf):
    """
    Computes the magnitude of the query vector for normalization.

    list_of_query_idf    List of query term idf values.
    return    Magnitude of the query vector.
    """
    query_norm = 1;
    for idf_value in list_of_query_idf:
        if not idf_value == 0:
            query_norm *= math.pow(idf_value, 2)
    return math.sqrt(query_norm)

#======================================================================#
# Load necessary files
#======================================================================#
def load_postings_and_list_of_imgIDs():
    """
    Loads the postings file in-memory and the list of imgIDs we are to search from

    return  List where:
            1st entry is the postings file
            2nd entry is the list of imgIDs
            3rd entry is the list of imgID's corresponding lengths
    """
    from_postings_file = open(postings_file, "r")
    return [pickle.load(from_postings_file),
            pickle.load(from_postings_file),
            pickle.load(from_postings_file)]

def load_visual_concept_classes():
    with open(classifications_file, 'rb') as file:
        reader = csv.reader(file)
        query_classifications = list(reader)
    file.close()
    return query_classifications

def get_query_visual_concept_text_tag(query_img_file_path):
    """
    Gets the list of visual concept classes this query image represents

    query_img_file_path    File path to the query image
    return    A list of Strings of this query image's visual concept classes
    """
    # Represents the image ID's text tag's file name
    query_img_text_tag_file_path = query_img_file_path[:-4] + ".txt"

    # Auxiliary variable to accumulate visual concept classes of this query img
    vc_classes_retrieved = []

    if (os.path.isfile(query_img_text_tag_file_path)):
        with open(query_img_text_tag_file_path, "r") as from_query_img_text_tag_file:
            # Process the concept_vector. Remove the last element as it is spoilt.
            concept_vector =  from_query_img_text_tag_file.readline().split(" ")[:-1]

            # List of indexes of text_tags that correspond to the 1000classification file
            text_tags_index_list = []

            # print "*** Index of concept class ***"
            for index, val in enumerate(concept_vector):
                if float(val) > 0:
                    # print "Excel spreadsheet index: " , str(index)
                    # Values > 0 mean that this img is highly related to the concept
                    # Remember to -1 in index because excel's row num  is 1-indexed
                    text_tags_index_list.append((index - 1, float(val)))
            # print "*** End printing index of concept class ***"

            # Sort the text_tags according to their concept relevance
            text_tags_index_sorted_list = \
                sorted(text_tags_index_list, key = lambda x: -x[1])

            # Get the corresponding visual classifications description for the
            # query image's text_tags index, but only use the top 5
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
    print "usage: " + sys.argv[0] + " -q path-to-query-img " +\
    "-p postings-file -c classifications-file -s semantic_feature_results"

# Initialize required variables to store file paths
query_img_file_path = query_img_name = postings_file = classifications_file = \
semantic_results_files= None

# Save file path arguments into their respective variables
try:
    opts, args = getopt.getopt(sys.argv[1:], 'q:p:c:s:')
except getopt.GetoptError, err:
    # Throw error in case user does not follow program input option format
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-q':
        query_img_file_path = a
    elif o == '-p':
        postings_file = a
    elif o == '-c':
        classifications_file = a
    elif o == '-s':
        semantic_results_files = a
    else:
        assert False, "unhandled option"
if query_img_file_path == None or classifications_file == None or \
    semantic_results_files == None or postings_file == None:
    print "Did you miss out any options?"
    print
    usage()
    sys.exit(2)

#=====================================================#
# Execution of Program
#=====================================================#

# Stop words of the English Dictionary by NLTK
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

# Chars we want to exclude
excluded_chars = ['']

# Load query classification table for each semantic visual concept
# This takes some time, so make a global variable
# TODO: Upon UI_search.py program initiation, load this up
visual_concept_classes = load_visual_concept_classes()

# ==============
# EXECUTION
# ==============

# Visual concepts
# execute(load_postings_and_list_of_imgIDs(), False, "zebra")

# Text-based query input only
execute(load_postings_and_list_of_imgIDs(), True)

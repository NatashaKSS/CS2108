import os
import getopt
import sys
import glob

#======================================================================#
# Program Description:
# Batch or singly generate the image paths for semanticFeature's use.
# The results will be written to: semantic_feature_extractor_file_names.txt
#
# Batch Example: .\write_query_file_paths.py -i ./queries -o batch
# Single Example: .\write_query_file_paths.py -i ./queries\0594_2309034355.jpg -o single
#======================================================================#
def single_process_semanticFeature():
    """
    Write the file name of an image to a text file meant for semanticFeature
    """
    # Write an image file name to a text file in the correct format
    with open(path_to_list_of_img_names, "w") as img_name_list_file:
        img_name_list_file.write(".\\\\" + query_img_file[2:] + "\n")
    img_name_list_file.close()

def batch_process_semanticFeature():
    """
    Write the file names of each image from a folder full of .jpg files to
    a text file meant for semanticFeature
    """
    # Get the list of image file names
    category_names = get_category_names()

    list_of_img_dirs = []
    for cat in category_names:
        path = query_img_file + "\\\\" + cat + "\\\\" + "/*.jpg"
        list_of_img_dirs.append(glob.glob(path))
    list_of_img_dirs = [item for sublist in list_of_img_dirs for item in sublist]

    # Write the list of image file names to a text file in the correct format
    with open(path_to_list_of_img_names, "w") as img_name_list_file:
        for img_dir in list_of_img_dirs:
            img_name_list_file.write(".\\\\" + img_dir[2:] + "\n")
    img_name_list_file.close()

def get_category_names():
    with open(path_to_list_of_cate_names, "r") as cate_names_file:
        lines = cate_names_file.readlines()
        lines = [x[:-1] for x in lines]
        cate_names_file.close()
        return lines
#======================================================================#
# Interpretation of program arguments
#======================================================================#
def usage():
    """
    'How-to-use' message in case user does not follow program input format
    """
    print "usage: " + sys.argv[0] + " -i path-to-imgs -o option to set "\
    "for running semanticFeature on a single image or a folder of images. "\
    "input 'single' for single image, 'batch' for batch folder of images."
    print "-----------------------------------------------------------"
    print "Example: .\write_query_file_paths.py -i ./queries -o single"
    print "-----------------------------------------------------------"

# Initialize required variables to store file paths
query_img_file = option = None

# Save file path arguments into their respective variables
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:')
except getopt.GetoptError, err:
    # Throw error in case user does not follow program input option format
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        query_img_file = a
    elif o == '-o':
        option = a
    else:
        assert False, "unhandled option"
if query_img_file == None or option == None:
    print "Did you miss out any options?"
    print "------------------------------"
    usage()
    sys.exit(2)

#=====================================================#
# Execution of Program
#=====================================================#
path_to_list_of_img_names = "semantic_feature_extractor_file_names.txt"
path_to_list_of_cate_names = "category_names.txt"

if option == "single":
    single_process_semanticFeature()
elif option == "batch":
    batch_process_semanticFeature()
else:
    print "Please input 'single' or 'batch' after the flag '-o'"

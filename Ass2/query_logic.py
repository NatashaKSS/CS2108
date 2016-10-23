import os, pickle, ntpath
from deeplearning.featureextracting.textual.compare_textual import CompareTextual

class QueryLogic:
    def __init__(self):
        # Gets the list of video file names from a directory
        # self.list_of_img_ids = os.listdir("./dataset")

        # Debug
        print("initialize QueryLogic class\n")
        self.venue_master = self.get_venue_classification("./venue-name.txt")

    def set_query_vid_path(self, filepath):
        self.query_path = filepath
        print(self.query_path)

    def set_query_vid_name(self, filename):
        self.query_videoname = filename
        print(self.query_videoname)

    def get_venue_classification(self, from_path):
        """
        Gets the master list of venues and returns a list contain their String
        names.
        Note: This list is 0-indexed while the master list is 1-index
        """
        audio_classes = []

        with open(from_path) as from_file:
            lines = from_file.readlines()
            for line in lines:
                index_venue_pair = line.split("\t")
                venue_index = int(index_venue_pair[0])
                venue_name = index_venue_pair[1][:-1] # gets rid of \n at back
                audio_classes.append(venue_name)
        return audio_classes

    def get_text_sorted_venues(self, venueindex_name_lst):
        venue_names = []
        for index, name in venueindex_name_lst:
            venue_names.append(self.venue_master[index - 1])
        return venue_names

    def get_search_results(self, switches, weights):
        """
        Input:
            toggle_search = [self.acoustic.get(), self.visual.get(), self.text.get()]
            audio_weights = [self.Emfcc.get(), self.Eenergy.get(), self.Ezerocrossing.get(), self.Emel.get()]
        """
        print("===========IN QUERYLOGIC.PY===========")
        print("=========QUERY VIDEO DETAILS==========")
        print("Query path: ", self.query_path)
        print("Query video name: ", self.query_videoname)
        print("Toggle switches: ", switches)
        print("Audio weight: ", weights)
        print("======================================")
        print("======DIAGNOSTIC INFO RESULTS=========")

        audio_results = []
        visual_results = []

        # pickle load AUDIO results
        with open('audio_results.pickle', 'rb') as to_file:
            audio_results = pickle.load(to_file)
        # print(audio_results)
        # print()

        # pickle load VISUAL results
        with open('save.txt', 'rb') as to_file:
            visual_results = pickle.load(to_file)
        print("Visual Dict: ", visual_results)
        print()

        # get TEXT results
        dataset_csv_path = 'vine-desc-training-results.txt'
        input_csv_path = 'vine-desc-validation-results.txt'
        classification_path = 'vine-venue-training.txt'
        input_classification_path = 'vine-venue-validation.txt'

        comparator = CompareTextual(input_csv_path, dataset_csv_path, input_classification_path)
        text_results = self.get_text_sorted_venues(comparator.get_category(self.query_videoname, 100))
        print("Text results: ", text_results)
        print()

        """
        Adjust the parameters HERE!!
        """
        # Based on checkboxes selected
        if (switches[0] == 1):
            # Visual keyword
            print("acoustic turned on")

        if (switches[1] == 1):
            # Color Histogram
            print("visual turned on")

        if (switches[2] == 1):
            # Visual Concept (image only)
            print("text turned on")

        return 0 # [final_venue, [list of umbrella group venues]]



    """
    From Assignment 1
    """
    def add_scores(self, accumulated_result, score_vector, scalar):
        """
        Adds up scores to a list that accumulates all the scores added so far,
        i.e. in 'accumulated_result'. Accepts scalar multiples (specified
        parameters) of scores you want to add as well.
        """
        if not len(score_vector) == 0:
            for img_ID, score in score_vector:
                if img_ID in accumulated_result.keys():
                    accumulated_result[img_ID] += float(scalar) * score
        return accumulated_result

    def get_image_attrs(self, file_path):
        """
        Process query image to feature vector
        """

        # initialize the image descriptor
        cd = colordescriptor.ColorDescriptor((4, 6, 2))

        # load the query image and describe it
        query = cv2.imread(file_path)
        queryfeatures = cd.describe(query)
        return queryfeatures

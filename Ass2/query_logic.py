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

        comparator = CompareTextual(dataset_csv_path, input_csv_path, classification_path)
        text_results = self.get_text_sorted_venues(comparator.get_category(self.query_videoname, 100))
        print("Text results: ", text_results)
        print()

        """
        Adjust the parameters HERE!!
        """
        # Default venues in case anything goes wrong
        final_venue = "Default"
        umbrella_group_title = "Default"
        umbrella_group_venues = ['Default', 'Nightclub', 'Hockey', 'Theme Park', 'Rock Club', 'Concert Hall', 'Theme Park', 'Music Venue']

        AUDIO_ONLY = (switches[0] == 1) and (switches[1] == 0) and (switches[2] == 0)
        VISUAL_ONLY = (switches[0] == 0) and (switches[1] == 1) and (switches[2] == 0)
        TEXT_ONLY = (switches[0] == 0) and (switches[1] == 0) and (switches[2] == 1)
        AUDIO_AND_VISUAL_ONLY = (switches[0] == 1) and (switches[1] == 1) and (switches[2] == 0)
        AUDIO_AND_VISUAL_AND_TEXT = (switches[0] == 1) and (switches[1] == 1) and (switches[2] == 1)

        # Based on checkboxes selected
        if (AUDIO_ONLY):
            # Audio ONLY
            print("acoustic only")
            final_venue = audio_results[self.query_videoname][0]

        if (VISUAL_ONLY):
            # Visual ONLY - returns the list of possible venues in its umbrella group
            print("visual only")
            umbrella_group_title = visual_results[self.query_videoname][0]
            umbrella_group_venues = visual_results[self.query_videoname][1]
        else:
            umbrella_group_venues = ""

        if (TEXT_ONLY):
            # Text ONLY
            print("text only")
            final_venue = text_results[0]

        if (AUDIO_AND_VISUAL_ONLY or AUDIO_AND_VISUAL_AND_TEXT):
            # Acoustic and Visual turned on
            print("acoustic and visual turned on")
            umbrella_group_title = visual_results[self.query_videoname][0]
            umbrella_group_venues = visual_results[self.query_videoname][1]

            # Note: Visual returns null, then just return the top result of acoustic
            final_venue = audio_results[self.query_videoname][0]
            for audio_venue in audio_results[self.query_videoname]:
                if audio_venue in umbrella_group_venues:
                    final_venue = audio_venue
                    break

        return [final_venue, umbrella_group_venues, umbrella_group_title]

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

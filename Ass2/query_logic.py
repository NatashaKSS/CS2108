import os, pickle, ntpath
# import colordescriptor
# import compute_search_score_of_vis_concepts as vconcept
# import compute_search_score_of_text_tags as text_engine

class QueryLogic:
    def __init__(self):
        # Gets the list of video file names from a directory
        # self.list_of_img_ids = os.listdir("./dataset")

        # Debug
        print("initialize QueryLogic class")

    def set_query_vid_path(self, filepath):
        self.query_path = filepath
        print(self.query_path)

    def set_query_vid_name(self, filename):
        self.query_videoname = filename
        print(self.query_videoname)

    def get_search_results(self, switches, query_text):
        results = []

        # Reminder: Every list of results produced by a Feature Extractor is
        # a list of the raw scores for every video, unranked. We will rank
        # all scores later.
        results_vis_concept_img = []
        results_vis_concept_text = []
        results_text_only = []

        # Initialize the final accumulated result list from all the Feature
        # Extractors selected by checkboxes below. This Dictionary will be
        # converted back to a list of tuples later on.
        accumulated_result = {}
        for ID in self.list_of_img_ids:
            accumulated_result[ID] = 0.0

        """
        Adjust the parameters (undecided which parameters yet...) here!!
        """
        if query_text == "":
            # Based on checkboxes selected
            if (switches[0] == 1):
                # Visual keyword
                a = 0.7

            if (switches[1] == 1):
                # Color Histogram
                b = 1.0

            if (switches[2] == 1):
                # Visual Concept (image only)
                c = 1.6
                results_vis_concept_img = \
                    vconcept.execute_vis_concept(self.query_path, \
                                                 self.vconcept_img_vectors)
                accumulated_result = \
                    self.add_scores(accumulated_result, \
                                    results_vis_concept_img, \
                                    c)
            if (switches[3] == 1):
                # Visual Concept (text only)
                d = 1.2

                results_vis_concept_text = \
                    text_engine.executeTextRetrieval( \
                        self.query_path, \
                        text_engine.load_postings_and_list_of_imgIDs(self.postings_path), \
                        True, self.visual_concept_classes)

                accumulated_result = \
                    self.add_scores(accumulated_result, \
                                    results_vis_concept_text, \
                                    d)

            # FINAL RESULTS IN [(IMG_ID, SCORE), (...,...), ...] format
            results = accumulated_result.items()

        else:
            # Text retrieval engine only
            results_text_only = \
                text_engine.executeTextRetrieval("", \
                    text_engine.load_postings_and_list_of_imgIDs(self.postings_path), \
                    False, [], query_text)

            results = results_text_only

        # Sort by the 2nd elem of each tuple (i.e. the raw score) in descending order
        results = sorted(results, key=lambda x: x[1], reverse=True)

        # Sometimes, the dataset contains the query image. Delete from results if so.
        if query_text == "": # Not for text retrieval
            for res in results:
                if res[0] == self.query_videoname:
                    results.remove(res)

        return results[:16] # Top 16 results

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

    """
    From Assignment 1
    """
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

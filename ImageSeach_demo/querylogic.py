import os, cv2, pickle
import colordescriptor, searcher

import compute_search_score_of_vis_concepts as vconcept
import compute_search_score_of_text_tags as text_engine
import keyword_matching as keyword_matcher

class QueryLogic:
    def __init__(self):
        self.list_of_img_ids = os.listdir("./dataset")

        # Color Histogram
        self.color_hist_searcher = searcher.Searcher("indexfull.csv") # ColorHist for Train

        # Visual Keyword
        from_vis_keyword_dataset_img_file = open("visual_keyword_des_dataset_images.txt", "r")
        self.list_surf_des = pickle.load(from_vis_keyword_dataset_img_file) # initialize

        # Visual Concept
        # For train set
        self.vconcept_img_vectors = vconcept.load_visual_concept_img_vectors("semanticpickle.txt")

        # For test set
        # self.vconcept_img_vectors = vconcept.load_visual_concept_img_vectors("semantictestpickle.txt")

        # Text retrieval
        self.trainset_postings_path = "trainset_text_tags_postings.txt"
        self.testset_postings_path = "testset_text_tags_postings.txt"
        self.visual_concept_classes = text_engine.load_visual_concept_classes()

    def set_query_img_path(self, filename):
        self.query_path = filename

    def set_color_hist_img_attrs(self):
        self.colHist_img_attrs = self.get_image_attrs(self.query_path)

    """
    0: VKeyword, 1: CHistogram, 2: VConcept(Img), 3: VConcept(Text)
    """
    def get_search_results(self, switches, query_text):
        results = []
        results_colHist = []
        results_vis_keyword = []
        results_vis_concept_img = []
        results_vis_concept_text = []
        results_text_only = []

        # Initialize the final accumulated result list from all the Feature
        # Extractors selected by checkboxes below. I used a Dictionary for
        # this as it is more convenient. This Dictionary will be converted back
        # to a list of tuples later on.
        accumulated_result = {}
        for ID in self.list_of_img_ids:
            accumulated_result[ID] = 0.0

        """
        Adjust the parameters a, b, c, d here!!
        """
        if query_text == "":
            # Based on checkboxes selected
            if (switches[0] == 1):
                # Visual keyword
                a = 1
                results_vis_keyword = keyword_matcher.keyword_matching(self.query_path, self.list_surf_des)
                accumulated_result = self.add_scores(accumulated_result, results_vis_keyword, a)
            if (switches[1] == 1):
                # Color Histogram
                b = 1
                results_colHist = self.color_hist_searcher.search(self.colHist_img_attrs)
                accumulated_result = self.add_scores(accumulated_result, results_colHist, b)
            if (switches[2] == 1):
                # Visual Concept (image only)
                c = 1
                results_vis_concept_img = vconcept.execute_vis_concept(self.query_path, self.vconcept_img_vectors)
                accumulated_result = self.add_scores(accumulated_result, results_vis_concept_img, c)
            if (switches[3] == 1):
                # Visual Concept (text only)
                d = 1
                results_vis_concept_text = \
                    text_engine.executeTextRetrieval(self.query_path, \
                        text_engine.load_postings_and_list_of_imgIDs(self.trainset_postings_path), True, self.visual_concept_classes)
                accumulated_result = self.add_scores(accumulated_result, results_vis_concept_img, d)

            # FINAL RESULTS IN [(IMG_ID, SCORE), (...,...), ...] format
            results = accumulated_result.items()

        else:
            # Text retrieval engine only
            results_text_only = \
                text_engine.executeTextRetrieval("", \
                    text_engine.load_postings_and_list_of_imgIDs(self.trainset_postings_path), False, [], query_text)
            results = results_text_only

        # Debug results
        # results = results_colHist
        # results = results_vis_keyword
        # results = results_vis_concept_img
        # results = results_vis_concept_text
        # results = results_text_only

        # Sort by the 2nd elem of each tuple (i.e. the raw score) in descending order
        results = sorted(results, key=lambda x: x[1], reverse=True)

        # return top 16
        return results[:16]

    def add_scores(self, accumulated_result, score_vector, scalar):
        if not len(score_vector) == 0:
            for img_ID, score in score_vector:
                accumulated_result[img_ID] += float(scalar) * score
        return accumulated_result

    def get_image_attrs(self, file_path):
        # process query image to feature vector
        # initialize the image descriptor
        cd = colordescriptor.ColorDescriptor((4, 6, 2))
        # load the query image and describe it
        query = cv2.imread(file_path)
        queryfeatures = cd.describe(query)
        return queryfeatures

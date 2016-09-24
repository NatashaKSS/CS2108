from .colordescriptor import ColorDescriptor
from .searcher import Searcher
import cv2

class QueryLogic:
    def get_image_attrs(self, file_path):
        # process query image to feature vector
        # initialize the image descriptor
        cd = ColorDescriptor((4, 6, 2))
        # load the query image and describe it
        query = cv2.imread(file_path)
        queryfeatures = cd.describe(query)
        return queryfeatures
    
    def get_search_results(self, queryfeatures):
        # perform the search
        #searcher = Searcher("index.csv")
        searcher = Searcher("indexfull.csv")
        results = searcher.search(queryfeatures)
        return results
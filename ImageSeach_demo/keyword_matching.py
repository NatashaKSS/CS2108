import cv2
import numpy as np
import operator

FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing

flann_params = dict(algorithm = FLANN_INDEX_KDTREE,
                    trees = 4)
list_surf_des = []
list_match_result = []

#To be used at initiation
def loadSurf(file_name):
    img1 = cv2.imread(file_name, 0)
    detector = cv2.SURF()
    kp1, des1 = detector.detectAndCompute(img1, None)
    list_surf_des.append((file_name, des1))


#To be used to obtain list of results
def keyword_matching(query_image):
    img2 = cv2.imread(query_image, 0)  # trainImage
    detector = cv2.SURF()
    # find the keypoints and descriptors with SIFT
    kp2, des2 = detector.detectAndCompute(img2, None)
    for i in range (len(list_surf_des)):
        des1 = list_surf_des[i][1]
        name = list_surf_des[i][0]
        #print len(des1)
        #print len(des2)
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        #print len(matches)
        count = 0.0
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                count += 1.0
        score = max(count/len(des1), count/len(des2))
        list_match_result.append([name, score])
    return list_match_result
import cv2
import numpy as np
import operator

FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing

flann_params = dict(algorithm = FLANN_INDEX_KDTREE,
                    trees = 4)
def match_flann(desc1, desc2, r_threshold = 0.6):
    flann = cv2.flann_Index(desc2, flann_params)
    idx2, dist = flann.knnSearch(desc1, 2, params = {}) # bug: need to provide empty dict
    mask = dist[:,0] / dist[:,1] < r_threshold
    idx1 = np.arange(len(desc1))
    pairs = np.int32( zip(idx1, idx2[:,0]) )
    return pairs[mask]

'''
def draw_matches(img1, kp1, img2, kp2, matches, color=None):
    """Draws lines between matching keypoints of two images.
    Keypoints not in a matching pair are not drawn.
    Places the images side by side in a new image and draws circles
    around each keypoint, with line segments connecting matching pairs.
    You can tweak the r, thickness, and figsize values as needed.
    Args:
        img1: An openCV image ndarray in a grayscale or color format.
        kp1: A list of cv2.KeyPoint objects for img1.
        img2: An openCV image ndarray of the same format and with the same
        element type as img1.
        kp2: A list of cv2.KeyPoint objects for img2.
        matches: A list of DMatch objects whose trainIdx attribute refers to
        img1 keypoints and whose queryIdx attribute refers to img2 keypoints.
        color: The color of the circles and connecting lines drawn on the images.
        A 3-tuple for color images, a scalar for grayscale images.  If None, these
        values are randomly generated.
    """
    # We're drawing them side by side.  Get dimensions accordingly.
    # Handle both color and grayscale images.
    if len(img1.shape) == 3:
        new_shape = (max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], img1.shape[2])
    elif len(img1.shape) == 2:
        new_shape = (max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1])
    new_img = np.zeros(new_shape, type(img1.flat[0]))
    # Place images onto the new image.
    new_img[0:img1.shape[0], 0:img1.shape[1]] = img1
    new_img[0:img2.shape[0], img1.shape[1]:img1.shape[1] + img2.shape[1]] = img2

    # Draw lines between matches.  Make sure to offset kp coords in second image appropriately.
    r = 15
    thickness = 2
    if color:
        c = color
    for m in matches:
        # Generate random color for RGB/BGR and grayscale images as needed.
        if not color:
            c = np.random.randint(0, 256, 3) if len(img1.shape) == 3 else np.random.randint(0, 256)
        # So the keypoint locs are stored as a tuple of floats.  cv2.line(), like most other things,
        # wants locs as a tuple of ints.
        end1 = tuple(np.round(kp1[m.trainIdx].pt).astype(int))
        end2 = tuple(np.round(kp2[m.queryIdx].pt).astype(int) + np.array([img1.shape[1], 0]))
        cv2.line(new_img, end1, end2, c, thickness)
        cv2.circle(new_img, end1, r, c, thickness)
        cv2.circle(new_img, end2, r, c, thickness)

    cv2.imwrite(new_img)
'''
'''
for i in range (200): #traverses through height of the image
    filename = str(i) + '.jpg'
    #print filename
    sample = cv2.imread(filename)
    # sampleGrey = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
    # Create SURF object. You can specify params here or later.
    # Here I set Hessian Threshold to 400
    detector = cv2.SURF(8000)
    # Find keypoints and descriptors directly
    kp, des = detector.detectAndCompute(sample,None)
    #print len(kp)
    detector.setHessianThreshold(50000)
    img2 = cv2.drawKeypoints(sample,kp,None,(255,0,0),4)

    #print img2
    filenameScan = 'scan' + str(i) + '.jpg'
    #cv2.imshow('sample', img2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    cv2.imwrite(filenameScan, img2)
'''
img1 = cv2.imread('01.jpg',0)          # queryImage
img2 = cv2.imread('scene.jpg',0) # trainImage
sample = img1
# sampleGrey = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
# Create SURF object. You can specify params here or later.
# Here I set Hessian Threshold to 400
detector2 = cv2.SURF(2000)
# Find keypoints and descriptors directly
kp, des = detector2.detectAndCompute(sample, None)
#print len(kp)


img1KP = cv2.drawKeypoints(sample, kp, None, (255, 0, 0), 4)
cv2.imwrite('zsample.jpg', img1KP)

# Initiate SURF detector
detector = cv2.SURF()

# find the keypoints and descriptors with SIFT
kp1, des1 = detector.detectAndCompute(img1,None)
kp2, des2 = detector.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in xrange(len(matches))]

# ratio test as per Lowe's paper
count = 0
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]
        count += 1

print count
nameOfMax = "none.jpg"
bestMatchNumber = 0.0
bestMatchList = {'none': 0}
listSize = 10
list_kptotal = []
for i in range (0,200): #traverses through height of the image
    filename = str(i) + '.jpg'
    #print filename
    sample = cv2.imread(filename)

    # Find keypoints and descriptors directly
    kp, des = detector.detectAndCompute(sample,None)
    #print len(kp)
    matches = flann.knnMatch(des1, des, k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in xrange(len(matches))]

    # ratio test as per Lowe's paper
    count = 0
    list_kp = []
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            count += 1
            img1_idx = matches[i][1].trainIdx
            (x1, y1) = kp[img1_idx].pt

    list_kptotal.append((x1, y1))
    if (min(bestMatchList.itervalues()) < count or len(bestMatchList) < listSize) :
        bestMatchNumber = count
        nameOfMax = filename
        bestMatchList[filename] = count
        if (len(bestMatchList) >= listSize):
            del bestMatchList[min(bestMatchList.iteritems(), key=operator.itemgetter(1))[0]]
#cv2.imwrite('match.jpg', img3)
print nameOfMax

for key, value in sorted(bestMatchList.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)
''' sample saerch
nameOfMax = "none.jpg"
bestMatchNumber = 0.0
bestMatchList = {'none': 0}
listSize = 10
for i in range (1,10): #traverses through height of the image
    filename = str(i) + '.jpg'
    #print filename
    sample = cv2.imread(filename)

    # Find keypoints and descriptors directly
    kp, des = detector.detectAndCompute(sample,None)
    #print len(kp)
    matchPoints = match_flann(des1, des, 0.6)

    matchRating = len(matchPoints)*1.0
    #print matchRating
    #print min(bestMatchList.itervalues())
    if (min(bestMatchList.itervalues()) < matchRating or len(bestMatchList) < listSize) :
        bestMatchNumber = len(matchPoints)*1.0
        nameOfMax = filename
        bestMatchList[filename] = matchRating
        if (len(bestMatchList) >= listSize):
            del bestMatchList[min(bestMatchList.iteritems(), key=operator.itemgetter(1))[0]]
#cv2.imwrite('match.jpg', img3)
print nameOfMax

for key, value in sorted(bestMatchList.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)
'''
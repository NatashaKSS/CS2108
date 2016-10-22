#Name: Adrian Chan
#Matric Number: A0122061

import cv2
import cv2.cv as cv
import os
imageType = 'training'
def load_training_video_classes(from_path):
    """
    Input:
        Path to the text file vine-venue-[training/validation].txt

    Output:
        Returns a {audio name : venue name} dictionary
        Note that "venue name" here is an index of the venue, referred to in
        "venue_name.txt", not a String.
    """
    audio_classes_dict = {}

    with open(from_path) as from_file:
        lines = from_file.readlines()
        for line in lines:
            audio_name_pair = line.split("\t")
            audio_name = audio_name_pair[0]
            venue_name = audio_name_pair[1][:-1] # gets rid of \n at back
            audio_classes_dict[audio_name] = venue_name
    return audio_classes_dict

name_file = load_training_video_classes('vine-venue-' + imageType + '.txt')

print name_file

def extractFrame(fileName) :
    fileNameMp4 = './vine/'+ imageType + '/' + fileName + '.mp4'
    cap = cv2.VideoCapture(fileNameMp4)
    frameCount = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
    count = 0
    frameMax = 5
    frameSkip = int(frameCount / frameMax)
#    newpath ='./vine/training/' + fileName
    newpath = './vine/'+ imageType + 'FrameQuery/' + fileName + "/"
    #print (newpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    for fr in range(1, frameCount):
        _, img = cap.read()
        if (fr % frameSkip == 0 or fr == frameCount - 1):
            frameName = newpath+ fileName +  "-frame" +str(count) + '.jpg'
            cv2.imwrite(frameName, img)
            count += 1
        if (count == frameMax):
            break
counter = 0
for key, value in name_file.iteritems():
    extractFrame(key)
    counter += 1
    if (counter%20 == 0) :
        print counter



#extractFrame('1000046931730481152')
'''
cap = cv2.VideoCapture('1003487942712397824.mp4')

width = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv.CV_CAP_PROP_FPS)
frameCount = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))


_,img = cap.read()
avgImg = np.float32(img)
count = 0
frameMax = 5
frameSkip = int(frameCount/frameMax)

for fr in range(1,frameCount):
    _, img = cap.read()
    cv2.accumulateWeighted(img, avgImg, 1.0/(fr+1))
    background = cv2.convertScaleAbs(avgImg)
    print "fr = ", fr, " alpha = ", 1.0/fr, fr == frameCount-1
    filename = str(fr) + '.jpg'
    if (fr%frameSkip ==0 or fr == frameCount-1):
        cv2.imwrite(filename, img)
        count += 1
    if (count == frameMax):
        break
'''
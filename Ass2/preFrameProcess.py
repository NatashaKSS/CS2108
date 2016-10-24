import os
import classify_visual as tfcv

type = 'validation'
maxLimit = 20
framePath = './vine/'+ type + 'FrameQuery/'
videoPath = './vine/'+ type + '/'


frameFiles = os.listdir(framePath)
videoFiles = os.listdir(videoPath)
counter = 0
for vF in videoFiles:
    fileName = framePath + vF[:-4]
    print (fileName)
    limit = tfcv.runVisualClassifier(fileName, vF[:-4], type, maxLimit)
    if (limit):
    	break
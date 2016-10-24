import os
import shutil
import pickle


def run(type):
    

    videoPath = './vine/'+ type + '/'
    destinationPath = './vine/'+ type + 'Processed/'
    videoFiles = os.listdir(videoPath)
    valids = pickle.load( open( "save.txt", "rb" ))

    counter = 0

    count = 0
    print (len(valids))
    for key in valids:
        
        video = videoPath + key + ".mp4"
        shutil.move(video, destinationPath)
        if (count %20 == 0):
            print (valids, "moved")
        count += 1
def moveSave(type):
    destinationPath = './vine/'+ type + 'Processed/save/'
    files = os.listdir(destinationPath)
    filename = destinationPath + 'saveProcessed' + str(len(files)+ 1) +'.txt'
    shutil.copy('save.txt', filename)
    open( "save.txt", "wb" ).close()
    print ('moved', filename)
'''
for key, value in image_file.iteritems():
    newpath = './vine/'+ imageType + 'FrameQuery/'
    searchpath = './vine/' + imageType + 'FrameQuery/' + key + '/'
    files = os.listdir(searchpath)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for f in files:
        imagepath = searchpath + f
        shutil.move(imagepath, newpath)
    if (count %20 == 0):
        print (count)
    count += 1
'''
#run('validation')
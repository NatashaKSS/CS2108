import tensorflow as tf
import sys
import os
import numpy as np
import pickle
import Arena as ArenaData

'''
image_path1 = framePath + '-frame0.jpg'
image_path2 = framePath + '-frame1.jpg'
image_path3 = framePath + '-frame2.jpg'
image_path4 = framePath + '-frame3.jpg'
image_path5 = framePath + '-frame4.jpg'

 image_set = [image_path1, image_path2, image_path3, image_path4, image_path5]
'''


def allValidationRead(image_address):
    image_set = []
    result = []
    print (image_address)
    for i in range(5):
        image_name = image_address + '-frame' + str(i) + '.jpg'
        image_set.append(image_name)
    result = run_visual_classifier(image_set)
    return result[0]

def searchAllImage(image_list):
    best = ["null", -1]
    for i in image_list:
        result = run_visual_classifier(i)
        if (best[1] < result[1] and (result[0] != 'face null')):
            best = result
    print (best)
    return best
def run_visual_classifier(image_list):

    # Read in the image_data
    result = []
    best = ["null", -1]

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile("output_labels.txt")]##a2

    # Unpersists graph from file
    with tf.gfile.FastGFile("output_graph.pb", 'rb') as f:##a2
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    for image_path in image_list:
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': image_data})
            
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            #thefile = open('visualMatch.txt', 'w')##a2
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                #print('%s (score = %.5f)' % (human_string, score))
                element = [human_string, score]
                result.append(element)
            #np.savetxt('visualMatch.txt', top_k)##a2
            print ('best valid search', result[0])
        output_sample = result[0]
        if (best[1] < output_sample[1] and (output_sample[0] != 'face null')):
            best = output_sample
        print (best)
        return best
def printDict(dictionary):
    '''
    for i in dictionary:
        print (i, " : ", dictionary[i])
    '''
    string = ""
    if (len(dictionary)%10 == 0):
        string = "["
        for i in dictionary:
            string = string +  str(i) + " , "
        string = string + " ] "
    print('Total so far = ', len(dictionary))
    print (string)
# MAIN=======================================

  
#valids = pickle.load( open( "save.txt", "rb" ))##a2
#venueDic = ArenaData.getDic()
#print(venueDic)

validsGlobal = {}

venueDic = {}

venueDic = ArenaData.getDic()
def load():
    if (os.stat("save.txt").st_size == 0):
        valids = {}
    else:
        valids = pickle.load( open( "save.txt", "rb" ))##a2    
    #print ('loaded valid')
    return valids



def runVisualClassifier(framePath, name, type, limit):
    venueDic = ArenaData.getDic()
    if (framePath != '-1'):
        validsGlobal = load()
        if (len(validsGlobal) == limit):
            return True
        #print('searching if file is in', not (name in validsGlobal))
        if not (name in validsGlobal):
            #print('loaded and preparing to search\n')
            printDict(validsGlobal)
            result = allValidationRead(framePath)
            print ('possible places', venueDic[result])
            value = [result, venueDic[result]]
            validsGlobal[name] = value
            #print('searched and preparing to save\n')
            printDict(validsGlobal)
            save(validsGlobal)
        
    return False
def save(validPickle):
    print ("SAVING ")
    open( "save.txt", "wb" ).close()
    pickle.dump(validPickle, open( "save.txt", "wb" ) )##a2






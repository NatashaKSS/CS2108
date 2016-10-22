import tensorflow as tf
import sys
import os
import numpy as np
import pickle
import Arena as ArenaData

'''
image_path1 = imagename + '-frame0.jpg'
image_path2 = imagename + '-frame1.jpg'
image_path3 = imagename + '-frame2.jpg'
image_path4 = imagename + '-frame3.jpg'
image_path5 = imagename + '-frame4.jpg'

 image_set = [image_path1, image_path2, image_path3, image_path4, image_path5]
'''


def allValidationRead(image_address):
    image_set = []
    result = []
    for i in range(5):
        image_name = image_address + '-frame' + str(i) + '.jpg'
        print (image_name)
        image_set.append(image_name)
    result = searchAllImage(image_set)
    return result[0]

def searchAllImage(image_list):
    best = ["null", -1]
    for i in image_list:
        result = run_visual_classifier(i)
        if (best[1] < result[1] and (result[0] != 'face null')):
            best = result
    print (best)
    return best
def run_visual_classifier(image_path):

    # Read in the image_data
    result = []
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line 
                       in tf.gfile.GFile("a2/output_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("a2/output_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
        
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        #thefile = open('a2/visualMatch.txt', 'w')
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            #print('%s (score = %.5f)' % (human_string, score))
            element = [human_string, score]
            result.append(element)
        #np.savetxt('a2/visualMatch.txt', top_k)
        print ('best valid search', result[0])
        return result[0]
    return result[0]

# MAIN=======================================

index = 2    
valids = pickle.load( open( "a2/save.txt", "rb" ))
venueDic = ArenaData.getDic()
print(venueDic)

print (valids)
if (sys.argv[1] == '-reset'):
    print ('reset results')
    valids = {}
while (sys.argv[index] != '-1'):
    imageName = sys.argv[index] 
    if not (imageName in valids):
        result = allValidationRead(imageName)
        print ('possible places', venueDic[result])
        value = [result, venueDic[result]]
        valids[imageName] = value
    index += 1
pickle.dump(valids, open( "a2/save.txt", "wb" ) )


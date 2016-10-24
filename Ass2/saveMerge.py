import os
import pickle

route = 'validation'
directory = './vine/' + route + 'Processed/save/'
saveFileSet = os.listdir(directory)
if (os.stat("save.txt").st_size == 0):
    valids = {}
else:
    valids = pickle.load(open("save.txt", "rb" ))##a2 

for f in saveFileSet:
	saveFile = directory + f
	print (saveFile)
	saveDic = pickle.load( open( saveFile, "rb" ))##a2 
	valids.update(saveDic)

pickle.dump(valids, open( "save.txt", "wb" ) )##a2

#valids = pickle.load( open( "save.txt", "rb" ))##a2 
print (len(valids))
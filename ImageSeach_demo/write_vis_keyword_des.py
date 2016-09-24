import pickle
import os
import keyword_matching as SURF

# Load visual descriptors for all images in dataset
list_surf_des = [] # initialize
for filename in os.listdir("./dataset"):
    list_surf_des.append(SURF.loadSurf("./dataset/" + filename, filename))

to_vk_file = open("visual_keyword_des_dataset_images.txt", "w")
pickle.dump(list_surf_des, to_vk_file)
to_vk_file.close()

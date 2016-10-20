import os

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

"""
Main program
"""
load_video_classification_path = "vine-venue-training.txt"
# load_video_classification_path = "vine-venue-validation.txt"

# Set up dictionary representing each video's y-truth value.
# dictionary in the form of { audio_name : venue_name } is returned
# Note: venue_name is the index of the venue that is referred to in "venue_name.txt"
audio_classes_dict = load_training_video_classes(load_video_classification_path)

# Renaming all files in the specified directory
path_to_data = "./deeplearning/data/audio/"
list_of_audio_names = os.listdir(path_to_data)
for audio_name in list_of_audio_names:
    audio_classification = audio_classes_dict[audio_name[:-4]]
    os.rename(path_to_data + audio_name, \
              path_to_data + audio_classification + "_" + audio_name)

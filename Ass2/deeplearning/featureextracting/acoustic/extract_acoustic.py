# __author__ = "xiangwang1223@gmail.com"
# The simple implementation of extracting multiple types of traditional acoustic features, consisting of Mel-Frequency Cepstral Coefficient (MFCC), Zero-Crossing Rate, Melspectrogram, and Root-Mean-Square features.

# Input: an original audio clip.
# Output: multiple types of acoustic features.
#   Please note that, 1. you need to select suitable and reasonable feature vector(s) to represent the video.
#                     2. if you select mfcc features, you need to decide how to change the feature matrix to vector.

# More details: http://librosa.github.io/librosa/tutorial.html#more-examples.

from __future__ import print_function
import moviepy.editor as mp
import librosa
import numpy as np
import os
import math
import json

"""
CHANGE THE NUMBER OF COLUMNS NEEDED HERE
"""
NUM_COLS = 250

# initialise boolean array for use later

bool_array = []
for i in range(NUM_COLS):
    bool_array.append(True)

def getAcousticFeatures(audio_reading_path):
    hop_length = 2048 # default is 512, resulting in about 280+ columns max, maybe sticking to powers of 2 is better?

    print("Processing:" + audio_reading_path)
    # 1. Load the audio clip;
    y, sr = librosa.load(audio_reading_path)

    # 2. Separate harmonics and percussives into two waveforms.
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    # 3. Beat track on the percussive signal.
    tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)

    """
    # 4. Compute MFCC features from the raw signal.
    feature_mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
    feature_mfcc = convertArray(feature_mfcc)
    print("MFCC Feature Done:", np.shape(feature_mfcc))

    # 5. Compute Melspectrogram features from the raw signal.
    feature_spect = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length, n_mels=128, fmax=80000)
    feature_spect = convertArray(feature_spect)
    print("Melspectrogram Feature Done:", np.shape(feature_spect))
    """

    # 6. Compute Zero-Crossing features from the raw signal.
    feature_zerocrossing = librosa.feature.zero_crossing_rate(y=y, hop_length=hop_length)
    feature_zerocrossing = convertArray(feature_zerocrossing)
    print("Zero-Crossing Rate:", np.shape(feature_zerocrossing))

    """
    # 7. Compute Root-Mean-Square (RMS) Energy for each frame.
    feature_energy = librosa.feature.rmse(y=y, hop_length=hop_length)
    feature_energy = convertArray(feature_energy)
    print("Energy Feature:", np.shape(feature_energy))
    # return feature_mfcc, feature_spect, feature_zerocrossing, feature_energy
    """

    return [], [], feature_zerocrossing, []

def convertArray(array):
    rows, cols = np.shape(array)

    num_repeats = math.ceil(NUM_COLS / cols)

    new_array = np.tile(array, (1, num_repeats))
    final_array = np.compress(bool_array, new_array, axis=1)

    return final_array

def maxPoolArray(array):
    return np.amax(array, axis=0, keepdims=True)

def meanPoolArray(array):
    return np.mean(array, axis=0, keepdims=True)

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

def save_all_audio_feature_vectors_to_text_file(data_to_train, file_name):
    """
    Input:
        feature    A ROW vector that represents this audio file's audio features
        file name  A String representing the output file's name

    Output:
        Produces a .txt file that contains the feature vector of every audio
        file and their corresponding y-truth value. Saves the .txt file to
        "../../feature/acoustic/data_train.txt"

        Every line of this .txt file contains the y-truth value integer, that is,
        an integer from 1 to 30 (according to the venues and their indices listed
        in "venue-name.txt") in the first entry, followed by the feature vector
        of this audio file.
    """
    storing_path = "../../feature/acoustic/" + file_name

    with open(storing_path, "w") as to_file:
        json.dump(data_to_train, to_file)

if __name__ == '__main__':
    list_of_audio_names = os.listdir("../../data/audio")
    print(list_of_audio_names, len(list_of_audio_names))

    """
    Note:
    YOU CAN CHANGE FILE PATHS FOR THIS PROGRAM HERE...
    """
    load_video_classification_path = "../../../vine-venue-validation.txt"
    # load_video_classification_path = "../../../vine-venue-validation.txt"

    save_all_audio_feature_vectors_path = "data_test_zero_crossing_only.txt"
    """
    END OF FILE PATH PARAMS TO CHANGE
    """

    # Set up dictionary representing each video's y-truth value.
    # dictionary in the form of { audio_name : venue_name } is returned
    # Note: venue_name is the index of the venue that is referred to in "venue_name.txt"
    audio_classes_dict = load_training_video_classes(load_video_classification_path)

    # Process every audio file in the directory
    counter = 1
    num_to_process = len(list_of_audio_names)
    all_audio_feature_vectors = []
    for audio_name in list_of_audio_names:
        print("You are now processing audio file " + str(counter) + "/" + str(num_to_process))
        audio_name = audio_name[:-4]

        # 1. Set the access path to the audio clip.
        audio_reading_path = "../../data/audio/" + str(audio_name) + ".wav"

        # 2. Fetch the corresponding features of the audio, consisting of mfcc, melspect, zero-crossing rate, and energy.
        feature_mfcc, feature_spect, feature_zerocrossing, feature_energy = \
            getAcousticFeatures(audio_reading_path=audio_reading_path)
        counter = counter + 1

        """
        IMPORTANT: PLEASE REMEMBER TO CHANGE THE VARIABLE TO BE SAVED IN
        [float(num) for num in list( <CHANGE VARIABLE HERE TO WHAT IS NEEDED> )]]]
        """
        # 3. Set the feature vector(s) we want to train the classifier with
        all_audio_feature_vectors.append( \
            [int(audio_classes_dict[audio_name]), [float(num) for num in list(feature_zerocrossing[0])]])

        print()

    save_all_audio_feature_vectors_to_text_file( \
        all_audio_feature_vectors, save_all_audio_feature_vectors_path)

    """
    # 3. Select the type of feature of interest, and set the storing path.
    acoustic_storing_path = "../../feature/acoustic/" + audio_name[:-4] + ".csv"

    # 4. Store the extracted acoustic feature(s) to .csv form.
    np.savetxt(acoustic_storing_path, \
               [feature_mfcc, feature_spect, feature_zerocrossing, feature_energy], \
               delimiter=",")
    """

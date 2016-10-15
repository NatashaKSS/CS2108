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

# initialise boolean array for use later

bool_array = []
for i in range(75):
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

    # 4. Compute MFCC features from the raw signal.
    feature_mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
    feature_mfcc = convertArray(feature_mfcc)
    print("MFCC Feature Done:", np.shape(feature_mfcc))

    # 5. Compute Melspectrogram features from the raw signal.
    feature_spect = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop_length, n_mels=128, fmax=80000)
    feature_spect = convertArray(feature_spect)
    print("Melspectrogram Feature Done:", np.shape(feature_spect))

    # 6. Compute Zero-Crossing features from the raw signal.
    feature_zerocrossing = librosa.feature.zero_crossing_rate(y=y, hop_length=hop_length)
    feature_zerocrossing = convertArray(feature_zerocrossing)
    print("Zero-Crossing Rate:", np.shape(feature_zerocrossing))

    # 7. Compute Root-Mean-Square (RMS) Energy for each frame.
    feature_energy = librosa.feature.rmse(y=y, hop_length=hop_length)
    feature_energy = convertArray(feature_energy)
    print("Energy Feature:", np.shape(feature_energy))
    
    print()

    return feature_mfcc, feature_spect, feature_zerocrossing, feature_energy


def convertArray(array):
    num_cols = 75
    
    rows, cols = np.shape(array)
    
    num_repeats = math.ceil(75 / cols)
    
    new_array = np.tile(array, (1, num_repeats))
    final_array = np.compress(bool_array, new_array, axis=1)
    
    return final_array


if __name__ == '__main__':
    list_of_audio_names = os.listdir("../../data/audio")
    print(list_of_audio_names)
    
    for audio_name in list_of_audio_names:
        # 1. Set the access path to the audio clip.
        audio_reading_path = "../../data/audio/" + audio_name

        # 2. Fetch the corresponding features of the audio, consisting of mfcc, melspect, zero-crossing rate, and energy.
        feature_mfcc, feature_spect, feature_zerocrossing, feature_energy = getAcousticFeatures(
            audio_reading_path=audio_reading_path)
        """
        # 3. Select the type of feature of interest, and set the storing path.
        acoustic_storing_path = "../../feature/acoustic/" + audio_name[:-4] + ".csv"

        # 4. Store the extracted acoustic feature(s) to .csv form.
        np.savetxt(acoustic_storing_path, feature_mfcc, delimiter=",")
        """
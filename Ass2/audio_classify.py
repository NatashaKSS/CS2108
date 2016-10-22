import pickle, json
import numpy as np
import scipy
from sklearn import svm
from sklearn import mixture
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from sklearn.metrics import classification_report

def get_venue_classification(from_path):
    audio_classes = []

    with open(from_path) as from_file:
        lines = from_file.readlines()
        for line in lines:
            index_venue_pair = line.split("\t")
            venue_index = int(index_venue_pair[0])
            venue_name = index_venue_pair[1][:-1] # gets rid of \n at back
            audio_classes.append(venue_name)
    return audio_classes

def get_ranked_venues(X_name_and_features):
    """
    Saves the audio file's ranked list of venues into a dictionary pickle
    { audio_name : ["City", "Concert Hall", ..., "Music Venue"] }
    """
    # Pre-process query feature vectors
    X_names = []
    X = []
    for sample in X_name_and_features:
        X_names.append(sample[0])
        # X.append(sample[1]) # Actual one when list of surprise queries comes in
        X.append(sample[2]) # For my own testing purposes first.

    # Load the model and predict the log probabilities of every video sample in X
    model = joblib.load('model.pkl')
    predicted_probs = model.predict_proba(X)

    venue_classification = get_venue_classification("./venue-name.txt")
    ranked_results = {}

    # Get the ranked list of venues
    ranked_venues = []
    for i, lst_of_probs in enumerate(list(predicted_probs)):
        ranked_indices = np.argsort(lst_of_probs)[::-1]
        ranked_venues.append([])
        for j in ranked_indices:
            ranked_venues[i].append(venue_classification[j])
        ranked_results[X_names[i]] = ranked_venues[i]

    # pickle dump results
    with open('audio_results.pickle', 'wb') as to_file:
        pickle.dump(ranked_results, to_file)

"""
Load validation set
"""
data_test_path = './deeplearning/feature/acoustic/Mel/data_test_spect_only_300_NEW.txt'
data_test = []
with open(data_test_path, 'r') as from_test_data_file:
    data_test = json.load(from_test_data_file)

print(get_ranked_venues(data_test))

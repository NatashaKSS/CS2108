import json
import os
import numpy as np
import numpy.random as nr
import scipy
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

def get_audio_names_classified(names, y):
    names_in_this_class = []
    indices = [i for i, x in enumerate(y) if x == 1.0]
    # print("list of indices classified with 1.0: ", indices)

    if not len(indices) == 0:
        for i in indices:
            names_in_this_class.append(names[i])
    else:
        return []
    return names_in_this_class

def get_audio_names_sets(names, y):
    sets_of_audio_venues = []

    for i in range(30):
        sets_of_audio_venues.append([])

    for i, y_classification in enumerate(y):
        sets_of_audio_venues[y_classification - 1].append(names[i])

    return sets_of_audio_venues

def compute_recall(sets_of_audio_venues, predicted_videos, venue_index):
    N = len(predicted_videos)
    if not N == 0:
        correct = 0
        for predicted_vid in predicted_videos:
            if predicted_vid in sets_of_audio_venues[venue_index]:
                correct = correct + 1
        print(str(correct) + "/" + str(N))
        return correct / N * 100
    else:
        return 0


"""
Load training set
"""
data_train_path = './deeplearning/feature/acoustic/data_train_energy_only_300.txt'
data_train = []
with open(data_train_path, 'r') as from_training_data_file:
    data_train = json.load(from_training_data_file)

# Pre-process Train Dataset
train_videos = []
X_train = []
y_train = []
for sample in data_train:
    train_videos.append(sample[0])
    y_train.append(sample[1])
    X_train.append(sample[2])

"""
Load validation set
"""
data_test_path = './deeplearning/feature/acoustic/data_test_energy_only_300.txt'
data_test = []
with open(data_test_path, 'r') as from_test_data_file:
    data_test = json.load(from_test_data_file)

# Pre-process Test Dataset
test_videos = []
X_test = []
y_test = []
for sample in data_test:
    test_videos.append(sample[0])
    y_test.append(sample[1])
    X_test.append(sample[2])

"""
Train our model and Evaluate on validation set
"""
num_train_samples = len(y_train)
num_test_samples = len(y_test)

# Initialize our set of y_train and y_test values for each classifier
# So for training data, list_of_y_train = [[],[],[],...]
# Each sublist contains 3000 entries of zeroes. There are 30 sublists.
# For test data, each sublist contains 900 entries of zeroes.
list_of_y_train = [list(np.zeros(num_train_samples)) for y in range(30)]
list_of_y_test = [list(np.zeros(num_test_samples)) for y in range(30)]

check_output_file = open('output_stuff.txt', 'w')
check_output_file.write("train videos: " + str(train_videos) + "\n")
check_output_file.write("y_train: " + str(y_train) + "\n")
check_output_file.write("num_train_samples: " + str(num_train_samples) + "\n")

check_output_file.write("test videos: " + str(test_videos) + "\n")
check_output_file.write("y_test: " + str(y_test) + "\n")
check_output_file.write("num_test_samples: " + str(num_test_samples) + "\n")

# Set up all the y_train and y_test values for each classifier to their
# corresponding y classification venue indices
for i, venue_index in enumerate(y_train):
    list_of_y_train[venue_index - 1][i] = 1.0

for i, venue_index in enumerate(y_test):
    list_of_y_test[venue_index - 1][i] = 1.0

# List of sets of audio names. Their indices represent their venue index.
sets_of_audio_venues_train = get_audio_names_sets(train_videos, y_train)
sets_of_audio_venues_test = get_audio_names_sets(test_videos, y_test)

# Train our linear classifier
for i in range(1):
    lin_classifier = svm.SVC(kernel='rbf').fit(X_train, list_of_y_train[i])
    print("For Venue " + str(i + 1))
    y_predicted_train = lin_classifier.predict(X_train)
    y_predicted_test = lin_classifier.predict(X_test)
    # print(list_of_y_train[i])
    #print(y_predicted_train[:500])
    #print(get_audio_names_classified(train_videos, y_predicted_train[:500]))
    print(y_predicted_test)
    #print(accuracy_score(y_predicted_train, y_train))
    print(accuracy_score(y_predicted_test, y_test))

    print("Acc Train: ")
    print(compute_recall(sets_of_audio_venues_train, \
                         get_audio_names_classified(train_videos, y_predicted_train),
                         i))
    print()
    print("Acc Test: ")
    print(compute_recall(sets_of_audio_venues_test, \
                         get_audio_names_classified(test_videos, y_predicted_test),
                         i))
    print()

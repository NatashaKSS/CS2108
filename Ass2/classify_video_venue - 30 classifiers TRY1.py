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

"""
Load training set
"""
data_train_path = './deeplearning/feature/acoustic/5_data_train_energy_only_300.txt'
data_train = []
with open(data_train_path, 'r') as from_training_data_file:
    data_train = json.load(from_training_data_file)

# Pre-process Train Dataset
X_train = []
y_train = []
for sample in data_train:
    y_train.append(sample[0])
    X_train.append(sample[1])

"""
Load validation set
"""
data_test_path = './deeplearning/feature/acoustic/5_data_test_energy_only_300.txt'
data_test = []
with open(data_test_path, 'r') as from_test_data_file:
    data_test = json.load(from_test_data_file)

# Pre-process Test Dataset
X_test = []
y_test = []
for sample in data_test:
    y_test.append(sample[0])
    X_test.append(sample[1])

"""
Train our model and Evaluate on validation set
"""
num_train_samples = len(y_train)
num_test_samples = len(y_test)

# Initialize our set of y_train and y_test values for each classifier
list_of_y_train = [list(np.zeros(num_train_samples)) for y in range(30)]
list_of_y_test = [list(np.zeros(num_test_samples)) for y in range(30)]

# Set up all the y_train and y_test values for each classifier to their
# corresponding y classification venue indices
for i in range(num_train_samples):
    y_classification_value = y_train[i]
    y_sublist = list_of_y_train[y_classification_value - 1]
    y_sublist[i] = 1
    list_of_y_train[y_classification_value - 1] = [int(num) for num in y_sublist]

for i in range(num_test_samples):
    y_classification_value = y_test[i]
    list_of_y_test[y_classification_value - 1][i] = 1

print(list_of_y_train)

audio_path = "./deeplearning/data/audio_train/" # Note, must end with the slash
list_of_audio_names = os.listdir(audio_path)

"""
check_output_file = open('output_stuff.txt', 'w')
lst_of_index = [i for i, x in enumerate(list_of_y_train[0]) if x == 1.0]
for i in lst_of_index:
    print(list_of_audio_names[i])

check_output_file.write(str(lst_of_index))
check_output_file.write(str(len(lst_of_index)))
check_output_file.close()
"""

# Train our linear classifier and write out the Ein and Eout scores
check_output_file = open('output_stuff.txt', 'w')
for i in range(30):
    print("Training Venue: " + str(i))
    lin_classifier = svm.SVC().fit(X_train, list_of_y_train[i])

    # print(lin_classifier.decision_function(X_train))

    # Print accuracy
    check_output_file.write("For Venue " + str(i) + ":\n")

    lst_of_index = [i for i, x in enumerate(lin_classifier.predict(X_train)) if x == 1.0]
    print("Hi")
    print(lin_classifier.predict(X_test))
    print("Bye")

    print(1 in lin_classifier.predict(X_train))
    print("***")
    print(lin_classifier.predict(X_train))
    print(list_of_y_train[i])
    print("***")
    print("---")

    y_train_predicted = [int(i) for i in lin_classifier.predict(X_train)]

    check_output_file.write("Acc_in :  " + str(accuracy_score(lin_classifier.predict(X_train), list_of_y_train[i])) + " | ")
    check_output_file.write("Acc_out: " + str(accuracy_score(lin_classifier.predict(X_test), list_of_y_test[i])) + "\n")
    check_output_file.write("\n")
check_output_file.close()

"""
# multi_class_classifier = OneVsRestClassifier(LinearSVC(C=100.0)).fit(X_train, y_train)
# multi_class_classifier = OneVsRestClassifier(svm.SVR(kernel='rbf', degree=3, gamma=0.1)).fit(X_train, y_train)
# multi_class_classifier = OneVsRestClassifier(svm.SVR(kernel='linear', C=1.0)).fit(X_train, y_train)

# Evaluate on Train set
print(str(multi_class_classifier.score(X_train, y_train)))
print(classification_report(y_train, multi_class_classifier.predict(X_train), target_names=None))

# Evaluate on Test set
print(str(multi_class_classifier.score(X_test, y_test)))
print(classification_report(y_test, multi_class_classifier.predict(X_test), target_names=None))
"""

"""
# Output some text for debug for easy viewing
check_output_file = open('output_scores_zero_crossing.txt', 'w')
check_output_file.write()
check_output_file.close()
"""

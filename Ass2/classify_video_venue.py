import json
import numpy as np
import numpy.random as nr
import scipy
from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

"""
Load training set
"""
data_train_path = './deeplearning/feature/acoustic/data_train_zero_crossing_only.txt'
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
data_test_path = './deeplearning/feature/acoustic/data_test_zero_crossing_only.txt'
data_test = []
with open(data_test_path, 'r') as from_test_data_file:
    data_test = json.load(from_test_data_file)

# Pre-process Test Dataset
X_test = []
y_test = []
for sample in data_test:
    y_test.append(sample[0])
    X_test.append(sample[1])

check_output_file = open('output_stuff.txt', 'w')
check_output_file.write(str(y_test))
check_output_file.write(str(X_test))
check_output_file.close()

"""
Train our model and Evaluate on validation set
"""
# multi_class_classifier = OneVsRestClassifier(LinearSVC(C=100.0)).fit(X_train, y_train)
multi_class_classifier = OneVsRestClassifier(svm.SVR(kernel='rbf', degree=3, gamma=0.1)).fit(X_train, y_train)
# multi_class_classifier = OneVsRestClassifier(svm.SVR(kernel='linear', C=1.0)).fit(X_train, y_train)

# Evaluate on Train set
print(str(multi_class_classifier.score(X_train, y_train)))
print(classification_report(y_train, multi_class_classifier.predict(X_train), target_names=None))

# Evaluate on Test set
print(str(multi_class_classifier.score(X_test, y_test)))
print(classification_report(y_test, multi_class_classifier.predict(X_test), target_names=None))

"""
# Output some text for debug for easy viewing
check_output_file = open('output_scores_zero_crossing.txt', 'w')
check_output_file.write()
check_output_file.close()
"""

import json
import numpy as np
import numpy.random as nr
import scipy
from sklearn import svm
from sklearn import mixture
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.metrics import log_loss

"""
Load training set
"""
data_train_path = \
    './deeplearning/feature/acoustic/MFCC/NEW_data_train_MFCC_only_300.txt'
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
data_test_path = \
    './deeplearning/feature/acoustic/MFCC/NEW_data_test_MFCC_only_300.txt'
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

check_output_file = open('output_stuff.txt', 'w')
check_output_file.write(str(y_test))
check_output_file.write(str(X_test))
check_output_file.close()

"""
Train our model using...
OneVsRestClassifier, SVM, RBF kernel
and Evaluate on validation set
"""
multi_class_classifier = OneVsRestClassifier(svm.SVR(kernel='rbf', degree=3, gamma=0.1)).fit(X_train, y_train)
# multi_class_classifier = OneVsRestClassifier(svm.SVR(kernel='linear')).fit(X_train, y_train)
# rbf kernel better

# Evaluate on Train set
print("\nTraining Data (in-sample) scores and classification_report: ")
print(str(multi_class_classifier.score(X_train, y_train)))
print(classification_report(y_train, multi_class_classifier.predict(X_train), target_names=None))

# Evaluate on Test set - Results written to disk
# Output classification_report and accuracy in-sample and out-of-sample
check_output_file = open(data_test_path + '-scores-rbf.txt', 'w')
check_output_file.write(str(multi_class_classifier.score(X_test, y_test)))
check_output_file.write(classification_report(y_test, multi_class_classifier.predict(X_test), target_names=None))
check_output_file.close()

"""
Train our model using...
GMM
and Evaluate on validation set
"""
"""
# multi_class_classifier = mixture.GMM(n_components=25).fit(X_train, y_train)
multi_class_classifier = RandomForestClassifier(n_estimators=1).fit(X_train, y_train)

# Evaluate on Train set
print("\nTraining Data (in-sample) scores and classification_report: ")
print(str(multi_class_classifier.score(X_train, y_train)))
multi_class_classifier_probs = multi_class_classifier.predict_proba(X_test)
sig_score = log_loss(y_test, multi_class_classifier_probs)
print("\nsig_score: " + str(sig_score) + "\n")
print(classification_report(y_train, multi_class_classifier.predict(X_train), target_names=None))
"""

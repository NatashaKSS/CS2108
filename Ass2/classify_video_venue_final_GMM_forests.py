import json
import numpy as np
import numpy.random as nr
import scipy
from sklearn import svm
from sklearn import mixture
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import log_loss

"""
Load training set
"""
data_train_path = './deeplearning/feature/acoustic/data_train_ALL_300_concat.txt'
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
data_test_path = './deeplearning/feature/acoustic/data_test_ALL_300_concat.txt'
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
GMM
and Evaluate on validation set

REMEMBER TO CHANGE THE OUTPUT FILE NAME. n100 (the portion at the
back of the name is n_estimators)
"""
# multi_class_classifier = mixture.GMM(n_components=25).fit(X_train, y_train)
multi_class_classifier = RandomForestClassifier(n_estimators=500).fit(X_train, y_train)

# Evaluate on Train set
print("\nTraining Data (in-sample) scores and classification_report: ")
print(str(multi_class_classifier.score(X_train, y_train)))
multi_class_classifier_probs = multi_class_classifier.predict_proba(X_test)
sig_score = log_loss(y_test, multi_class_classifier_probs)
print("\nsig_score: " + str(sig_score) + "\n")
print(classification_report(y_train, multi_class_classifier.predict(X_train), target_names=None))

# Our prediction
test_prediction = multi_class_classifier.predict(X_test)
print(test_prediction, len(test_prediction))

# Export and save the model for future use so you don't need to train again
# joblib.dump(multi_class_classifier, 'model.pkl', compress=9)

# Evaluate on Test set - Results written to disk
# Output classification_report and accuracy in-sample and out-of-sample
check_output_file = open(data_test_path + '-scores-forests-n500.txt', 'w')
check_output_file.write(str(multi_class_classifier.score(X_test, y_test)))
check_output_file.write(classification_report(y_test, test_prediction, target_names=None))
check_output_file.close()
"""
check_output_file = open('output_predict_probab.txt', 'w')
check_output_file.write("\n")
check_output_file.write(str(list(multi_class_classifier.predict_proba(X_test))))
check_output_file.write("\n Predict Proba len")
check_output_file.write(str(len(multi_class_classifier.predict_proba(X_test))))
check_output_file.write("\n Predict Proba len 1st")
check_output_file.write(str(len(multi_class_classifier.predict_proba(X_test)[0])))
check_output_file.close()
"""

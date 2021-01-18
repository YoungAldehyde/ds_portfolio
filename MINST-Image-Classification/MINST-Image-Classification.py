from scipy.io import loadmat
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import sklearn.svm as svm
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
from sklearn.utils import resample
from scipy.spatial import distance
from sklearn.metrics.pairwise import euclidean_distances

filename=".\\mnist_10digits.mat"
digits = loadmat(filename)

X_train = digits['xtrain']
X_test = digits['xtest']
y_train = digits['ytrain'].T.ravel()
y_test = digits['ytest'].T.ravel()

#standarize the features
X_train = X_train/255
X_test = X_test/255


X_train_sample, y_train_sample = resample(X_train, y_train, n_samples = 5000, random_state=0)


#LR
method_name = 'Logistic_Regression'
clf = LogisticRegression()
clf.fit(X_train_sample, y_train_sample)

predictions = clf.predict(X_test)

cm = metrics.confusion_matrix(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

cr = metrics.classification_report(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

print(method_name,'\n')
print('Confusion matrix: \n')
print(cm,'\n')

print('Precision, Recall, and F-1 score: \n')
print(cr,'\n')

#KNN
method_name = 'KNN'
clf = KNeighborsClassifier(10)
clf.fit(X_train_sample, y_train_sample)

predictions = clf.predict(X_test)

cm = metrics.confusion_matrix(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

cr = metrics.classification_report(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

print(method_name,'\n')
print('Confusion matrix: \n')
print(cm,'\n')

print('Precision, Recall, and F-1 score: \n')
print(cr,'\n')

#Linear SVM
method_name = 'Linear_SVM'
clf = svm.SVC(kernel='linear')
clf.fit(X_train_sample, y_train_sample)

predictions = clf.predict(X_test)

cm = metrics.confusion_matrix(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

cr = metrics.classification_report(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

print(method_name,'\n')
print('Confusion matrix: \n')
print(cm,'\n')

print('Precision, Recall, and F-1 score: \n')
print(cr,'\n')

#Kernal SVM
method_name = 'Kernal_SVM'

#reduce the training set for the median trick
X_train_sample_kernal_svm_median_trick, y_train_sample_kernal_svm_median_trick = resample(X_train_sample, y_train_sample, n_samples = 1000, random_state=0)

#Median trick to find a good gamma
training_distances = euclidean_distances(X_train_sample_kernal_svm_median_trick,X_train_sample_kernal_svm_median_trick) #compute pair-wise euclidean distances of reduced training sample (1000)
M = np.median(training_distances) #compute median of the distances
sigma = np.sqrt(M/2)
gamma = 1/(np.power((2*sigma),2))

clf = svm.SVC(kernel='rbf',
             C = 1.0, 
             gamma = gamma)

clf.fit(X_train_sample, y_train_sample)

predictions = clf.predict(X_test)

cm = metrics.confusion_matrix(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

cr = metrics.classification_report(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

print(method_name,'\n')
print('Confusion matrix: \n')
print(cm,'\n')

print('Precision, Recall, and F-1 score: \n')
print(cr,'\n')


#NN
method_name = 'Neural_Nets'
clf = MLPClassifier(alpha=0.1, max_iter=1000, hidden_layer_sizes = (20, 10))
clf.fit(X_train_sample, y_train_sample)

predictions = clf.predict(X_test)

cm = metrics.confusion_matrix(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

cr = metrics.classification_report(y_true=y_test, 
                         y_pred = predictions, 
                        labels = clf.classes_)

print(method_name,'\n')
print('Confusion matrix: \n')
print(cm,'\n')

print('Precision, Recall, and F-1 score: \n')
print(cr,'\n')
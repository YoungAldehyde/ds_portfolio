import pandas as pd
import numpy as np
from numpy.random import RandomState
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn import model_selection
import sklearn.svm as svm
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pylab as plt


df = pd.read_csv('data/spambase.data', header=None)

X = df.iloc[:, :-1]
y = df.iloc[:,-1:]

# Create Decision Tree classifer object
clf = DecisionTreeClassifier(
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=10,)

# Train Decision Tree Classifer
clf = clf.fit(X,y)

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,class_names=['not_spam','spam'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('spam_dtree.png')
Image(graph.create_png())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1) 

#decision tree
#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("classification test error rate:",1 - metrics.accuracy_score(y_test, y_pred))


# Create RF classifer object
clf = RandomForestClassifier(max_depth=5,
    min_samples_split=10,
    min_samples_leaf=10,)

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Random forest
#Predict the response for test dataset
y_pred = clf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("classification test error rate:",1 - metrics.accuracy_score(y_test, y_pred))

# iterate number of trees 1~50
dic = {}

for i in range(1,101):

    clf = RandomForestClassifier(max_depth=5,
        min_samples_split=10,
        min_samples_leaf=10,
        n_estimators = i)

    clf = clf.fit(X_train,y_train)
    
    y_pred = clf.predict(X_test)
    
    dic[i] = 1 - metrics.accuracy_score(y_test, y_pred)



lists = sorted(dic.items()) # sorted by key, return a list of tuples

n_tree, classification_test_error_rate = zip(*lists) # unpack a list of pairs into two tuples

plt.plot(n_tree, classification_test_error_rate, label = 'RF classification_test_error_rate')
plt.axhline(y=0.08360477741585237,ls = '--',label='CART classification test error rate') #from the pruned decision tree
plt.legend()
plt.show()


#omly keep non_spams in the new training set
y_train_non_spams = y_train[y_train[57] == 0]

X_train_non_spams = X_train.loc[y_train_non_spams.index, : ]

#One class svm
clf = svm.OneClassSVM(kernel="rbf",nu=0.02)#, gamma=0.1)
             
clf = clf.fit(X_train_non_spams)
#y_pred_train = clf.predict(X_train_non_spams)
y_pred_test = clf.predict(X_test)

# Transform the prediction labels so that non-spam is 0 and spam is 1. 
y_pred_test[y_pred_test == 1] = 0    #non spam
y_pred_test[y_pred_test == -1] = 1  # spam

print("total misclassification error rate: ", 1 - metrics.accuracy_score(y_test, y_pred_test))
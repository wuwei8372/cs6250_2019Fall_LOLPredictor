from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import export_graphviz
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from learner import get_data

X_train, X_test, y_train, y_test = get_data()

max_depth_list = [1, 2, 3, 4, 5, 6, 7, 8]
n_estimators_list = [5, 10, 50, 100]

plt.figure()
for max_depth in max_depth_list:
    training_scores = []
    testing_scores = []
    for n_estimators in n_estimators_list:
        lr = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators)
        lr.fit(X_train, y_train)
        training_scores += [1 - lr.score(X_train, y_train)]
        testing_scores += [1 - lr.score(X_test, y_test)]
    plt.plot(n_estimators_list, testing_scores, label='max_depth:' + str(max_depth))
plt.legend(loc='auto')
plt.xlabel('n_estimators')
plt.ylabel('error')
plt.savefig('error_vs_estimator')

plt.figure()
for n_estimators in n_estimators_list:
    training_scores = []
    testing_scores = []
    for max_depth in max_depth_list:
        lr = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators)
        lr.fit(X_train, y_train)
        training_scores += [1 - lr.score(X_train, y_train)]
        testing_scores += [1 - lr.score(X_test, y_test)]
    plt.plot(max_depth_list, testing_scores, label='n_estimators:' + str(n_estimators))
plt.legend(loc='auto')
plt.xlabel('max_depth')
plt.ylabel('error')
plt.savefig('error_vs_depth')
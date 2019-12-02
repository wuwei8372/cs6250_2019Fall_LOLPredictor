"""
==================================
Comparing various online solvers
==================================

An example showing how different online solvers perform
on the hand-written digits dataset.

"""
# Author: Rob Zinkov <rob at zinkov dot com>
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier, Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import LogisticRegression



from learner import get_data, get_model
import pandas as pd

X_train, X_test, y_train, y_test = get_data()
lr = get_model(X_train, X_test, y_train, y_test)
X, y = pd.concat([X_train, X_test]), pd.concat([y_train, y_test])

heldout = [0.95, 0.90, 0.75, 0.50, 0.01]
rounds = 3 # 20

classifiers = [
    ("SGD", SGDClassifier(loss='log', warm_start=False)),
    ("ASGD", SGDClassifier(loss='log', warm_start=False, average=True)),
    ("SAGA", lr)
]

xx = 1. - np.array(heldout)

for name, clf in classifiers:
    print("training %s" % name)
    rng = np.random.RandomState(42)
    yy = []
    for i in heldout:
        yy_ = []
        for r in range(rounds):
            X_train, X_test, y_train, y_test = \
                train_test_split(X, y, test_size=i, random_state=rng)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            yy_.append(1 - np.mean(y_pred == y_test))
        yy.append(np.mean(yy_))
    plt.plot(xx, yy, label=name)

plt.legend(loc="upper right")
plt.xlabel("Proportion train")
plt.ylabel("Test Error Rate")
plt.savefig('online')

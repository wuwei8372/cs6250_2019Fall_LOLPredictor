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

f = open("large.txt", "r")
# 100,000
df = pd.DataFrame()

data = []
for x in f:
    line = x.split("\t")
    ran = random.randint(0, 1)
    if ran == 0:
        data.append([int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]),
                     int(line[6]), int(line[7]), int(line[8]), int(line[9]), int(line[10]), 1])
    else:
        data.append([int(line[6]), int(line[7]), int(line[8]), int(line[9]), int(line[10]),
                     int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]), 0])

df = pd.DataFrame(data, columns=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'result'])
X = df[['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10']]

y = df['result']

total_size = len(y)
data_size_list = 1000 * np.array(range(1, 10)) + (total_size * np.array(range(1, 10)) // 10).tolist()
training_scores = []
testing_scores = []
for data_size in data_size_list:
    np.random.seed(0)
    indices = np.random.choice(total_size, size=data_size, replace=False)
    X_train, X_test, y_train, y_test = train_test_split(X.iloc[indices], y.iloc[indices],
                                                        test_size=0.25, random_state=0)

    lr = RandomForestClassifier(max_depth = 10, n_estimators = 10)
    """
    lr = LogisticRegression(solver='saga', multi_class='ovr',
                                    warm_start=False, max_iter=1000,
                                    penalty='elasticnet', l1_ratio=1)
    """
    lr.fit(X_train, y_train)
    training_scores += [1 - lr.score(X_train, y_train)]
    testing_scores += [1 - lr.score(X_test, y_test)]

# plt.title(s='auto', label='Accuracy')
plt.figure()
plt.plot(data_size_list, training_scores, color="blue", label='training')
plt.plot(data_size_list, testing_scores, color="red", label='testing')
plt.legend(loc='auto')
plt.xlabel('data size')
plt.ylabel('error')
plt.savefig('accuracy_vs_data_size')

""""
test_size_list = np.array(range(1, 10)) / 10

training_scores = []
testing_scores = []
for test_size in test_size_list:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)

    lr = LogisticRegression(solver='saga', multi_class='ovr',
                                warm_start=False, max_iter=1000,
                                penalty='elasticnet', l1_ratio=1)
    lr.fit(X_train, y_train)

    training_scores += [lr.score(X_train, y_train)]
    testing_scores += [lr.score(X_test, y_test)]

plt.figure(figsize=(10,6), dpi=80)
plt.plot(test_size_list, training_scores, color="blue", linewidth=2.5, linestyle="-")
plt.plot(test_size_list, testing_scores, color="red",  linewidth=2.5, linestyle="-")
plt.savefig('test_size')
"""
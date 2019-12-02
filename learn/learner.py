import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
# from sklearn.externals import joblib
import random
from sklearn import set_config
import sklearn
print('The scikit-learn version is {}.'.format(sklearn.__version__))
# 0.21.3
# pip3 install -U scikit-learn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
from sklearn.metrics import (brier_score_loss, precision_score, recall_score, f1_score)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve

def plot_feature_transformation(clf_test):
    plt.figure(figsize=(10, 7))
    plt.plot([0, 1], [0, 1], 'k--')
    for clf, X_test, y_test, label in clf_test:
        y_pred = clf.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred)
        plt.plot(fpr, tpr, label=label)
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.savefig('feature_transformation')

def plot_compare_calibration(clf_test):
    plt.figure(figsize=(10, 10))
    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))

    ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")

    for clf, X_test, y_test, name in clf_test:
        y_pred = clf.predict(X_test)
        prob_pos = clf.predict_proba(X_test)[:, 1]
        clf_score = brier_score_loss(y_test, prob_pos, pos_label=1)
        print("%s:" % name)
        print("\tBrier: %1.3f" % (clf_score))
        print("\tPrecision: %1.3f" % precision_score(y_test, y_pred))
        print("\tRecall: %1.3f" % recall_score(y_test, y_pred))
        print("\tF1: %1.3f\n" % f1_score(y_test, y_pred))

        fraction_of_positives, mean_predicted_value = \
            calibration_curve(y_test, prob_pos, n_bins=10)

        ax1.plot(mean_predicted_value, fraction_of_positives, "s-",
                 label="%s (%1.3f)" % (name, clf_score))

        ax2.hist(prob_pos, range=(0, 1), bins=10, label=name,
                 histtype="step", lw=2)

    ax1.set_ylabel("Fraction of positives")
    ax1.set_ylim([-0.05, 1.05])
    ax1.legend(loc="lower right")
    ax1.set_title('Calibration plots  (reliability curve)')

    ax2.set_xlabel("Mean predicted value")
    ax2.set_ylabel("Count")
    ax2.legend(loc="upper center", ncol=2)

    plt.tight_layout()
    plt.savefig('calibration.png')

def get_data():
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
    return X_train,X_test,y_train,y_test

def get_model_lr(X_train, X_test, y_train, y_test):
    """ same
    for C in [0.001, 0.01, 0.1, 1, 10, 100, 1000]:
        for l1_ratio in [0, 0.25, 0.5, 0.75, 1.0]:
            lr = LogisticRegression(solver='saga', multi_class='ovr',
                                    warm_start=False, C=C,
                                    penalty='elasticnet', l1_ratio=l1_ratio)
            lr.fit(X_train, y_train)
            print('Accuracy: ', lr.score(X_test, y_test))
    """
    lr = LogisticRegression(solver='saga', multi_class='ovr',
                            warm_start=False, max_iter=1000,
                            penalty='elasticnet', l1_ratio=1)
    print(lr)
    lr.fit(X_train, y_train)
    return lr, X_test, y_test

def get_model_rf(X_train, X_test, y_train, y_test):
    """
    for max_depth in np.array(range(1,10)):
        rf = RandomForestClassifier(max_depth=max_depth)
        rf.fit(X_train, y_train)
        print(max_depth, rf.score(X_test, y_test))
    """
    rf = RandomForestClassifier(max_depth=3, n_estimators=10)
    rf.fit(X_train, y_train)
    print(rf)
    return rf, X_test, y_test

def get_model(X_train, X_test, y_train, y_test):
    X_train_rf, X_train_lr, y_train_rf, y_train_lr = train_test_split(X_train, y_train, test_size=0.5)
    rf, _, _ = get_model_rf(X_train_rf, X_test, y_train_rf, y_test)

    rf_enc = OneHotEncoder(categories='auto')
    rf_enc.fit(rf.apply(X_train_rf))
    X_train_lr, X_test = rf_enc.transform(rf.apply(X_train_lr)), rf_enc.transform(rf.apply(X_test))

    lr, _, _ = get_model_lr(X_train_lr, X_test, y_train_lr, y_test)

    return lr, X_test, y_test

def main():
    X_train, X_test, y_train, y_test = get_data()

    lr, X_test_lr, y_test_lr = get_model_lr(X_train, X_test, y_train, y_test)
    rf, X_test_rf, y_test_rf = get_model_rf(X_train, X_test, y_train, y_test)
    lr_rf, X_test, y_test = get_model(X_train, X_test, y_train, y_test)

    plot_compare_calibration([
        [lr, X_test_lr, y_test_lr, 'LR'],
        [rf, X_test_rf, y_test_rf, 'RF'],
        [lr_rf, X_test, y_test, 'RF + LR']
    ])

    plot_feature_transformation([
        [lr, X_test_lr, y_test_lr, 'LR'],
        [rf, X_test_rf, y_test_rf, 'RF'],
        [lr_rf, X_test, y_test, 'RF + LR']
    ])

    exit(0)
    set_config(print_changed_only=True)

    filename = 'finalized_model.sav'
    joblib.dump(logistic_regression, filename)

if __name__ == "__main__":
    main()
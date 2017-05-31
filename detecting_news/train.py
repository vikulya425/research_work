import pandas as pd
import numpy as np
import features
from sklearn import metrics
from sklearn.cross_validation import KFold
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import label_binarize
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction import DictVectorizer

if __name__ == "__main__":

    train = pd.read_csv('train.csv', header=0, index_col='number')

    y = train['type']
    #print(len(y))
    x = train.drop('type', axis=1)
    #x = x.drop(('number'), axis=1)
    kf = KFold(len(y), n_folds=5)
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=1)

    clf1 = LogisticRegression(penalty='l2',C = 0.00001)
    clf2 = GaussianNB()
    clf3 = RandomForestClassifier()
    clf3.fit(X_train, y_train)

    #print(confusion_matrix(y_test, clf.predict(X_test)))
    scores = cross_val_score(clf3, x, y, scoring='accuracy', cv=kf)
    print((scores.mean(), scores.std() * 2))
    scores = cross_val_score(clf3, x, y, scoring='roc_auc', cv=kf)
    print((scores.mean(), scores.std() * 2))
    #cross_val_score
    predicted = clf3.predict(x)
    print(metrics.accuracy_score(y, predicted))
    print(metrics.f1_score(y, predicted))
    print(metrics.recall_score(y, predicted))
    print(metrics.precision_score(y, predicted))

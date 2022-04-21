import numpy as np
from sklearn import datasets
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.preprocessing import PolynomialFeatures

import datetime
now=datetime.datetime.now()
print('20191320 권순혁 현재시간:{}'.format(now))

#svm분류기
from sklearn.tree import DecisionTreeClassifier

iris = datasets.load_iris()
X = iris["data"][:, (2, 3)] # petal length, petal width
y = (iris["target"] == 2).astype(np.float64) # Iris-Virginica
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, shuffle=True, random_state=0)# 테스트셋 구분
svm_clf = Pipeline((#분류기 생성
("scaler", StandardScaler()),
("linear_svc", LinearSVC(C=1, loss="hinge")),
))
svm_clf.fit(X_train, y_train)#테스트데이터학습
y_pred=svm_clf.predict(X)#샘플데이터 예측
print(accuracy_score(y,y_pred))#예측 점수 출력

#svm없이
polynomial_svm_clf = Pipeline((#분류기 생성
("poly_features", PolynomialFeatures(degree=3)),
("scaler", StandardScaler()),
("svm_clf", LinearSVC(C=10))
))
polynomial_svm_clf.fit(X_train, y_train)
y_pred2=svm_clf.predict(X)#샘플데이터 예측
print(accuracy_score(y,y_pred2))#예측 점수 출력

from sklearn.svm import SVC

poly_kernel_svm_clf = Pipeline((
("scaler", StandardScaler()),
("svm_clf", SVC(kernel="poly", degree=3, C=5))))
poly_kernel_svm_clf.fit(X_train, y_train)
y_pred3=svm_clf.predict(X)#샘플데이터 예측
print(accuracy_score(y,y_pred3))#예측 점수 출력

rbf_kernel_svm_clf = Pipeline((
("scaler", StandardScaler()),
("svm_clf", SVC(kernel="rbf", gamma=5, C=1))
))
rbf_kernel_svm_clf.fit(X_train, y_train)
y_pred4=svm_clf.predict(X)#샘플데이터 예측
print(accuracy_score(y,y_pred4))#예측 점수 출력

clfone = OneVsOneClassifier(LinearSVC(random_state=0,max_iter=1000000)).fit(X_train, y_train)
clfrest = OneVsRestClassifier(LinearSVC(random_state=0,max_iter=1000000)).fit(X_train, y_train)
predictedone = clfone.predict(X_test)
print(accuracy_score(y_test,predictedone))
predictedrest = clfrest.predict(X_test)
print(accuracy_score(y_test,predictedrest))

#Decision Tree

iris = load_iris()
print(iris.feature_names)
X = iris.data[:, 2:] # petal length and width
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

tree_clf = DecisionTreeClassifier(max_depth=3)
tree_clf.fit(X_train, y_train)
y_pred=tree_clf.predict(X_test)#샘플데이터 예측
print(accuracy_score(y_test,y_pred))#예측 점수 출력

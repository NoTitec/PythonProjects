import os

import pandas as pd
import sklearn.preprocessing
from sklearn.datasets import fetch_openml
from six.moves import urllib #url에서 원하는 데이터 csv 파일 다운로드
import numpy as np# 행렬 연산
from sklearn import datasets # 샘플데이터로드
from sklearn import preprocessing # 수치데이터 bool데이터 변환, 정규화 변환
from sklearn.model_selection import train_test_split # 학습데이터 테스트 데이터 불류 모듈
from sklearn.preprocessing import MinMaxScaler # 스케일링
from sklearn.preprocessing import LabelEncoder # 라벨 인코더

#이진화
input_data = np.array([[3.1, -1.6, 2.3], [-2.4, 6.5, -4.4], [3.5, 1.1, 2.0]])
binarized_data=preprocessing.Binarizer(threshold=2.0).transform(input_data) # threshold왜 빨간색인진 모르지만 작동은 잘됨

print("이진 데이터 : \n", binarized_data)


#평균 제거
print("평균 제거 이전 :")
print("평균 = ", input_data.mean(axis=0))
print("표준편차 = ", input_data.std(axis=0))

scaled_data =  preprocessing.scale(input_data)
print("평균 제거 이후 :")
print("평균 = ", scaled_data.mean(axis=0))#정확히 0은아니지만 한없이 0에 가까움
print ("표준편차 = ", scaled_data.std(axis=0))

#스케일링
my_data = np.array([10, 3, 56, 567, 30],dtype="float").reshape(-1, 1)# reshape로 1개씩 뽑아서 뽑은개수만큼의 행가진 matrix 반환
minmax_scaler = MinMaxScaler()# MinMax 객체생성
minmax_scaler.fit(my_data) # 내 데이터 분석
print(str(minmax_scaler.data_min_) + " ~ " + str(minmax_scaler.data_max_))
scaled_my_data = minmax_scaler.transform(my_data)
print(scaled_my_data)

#표준 스케일링
# 평균제거법과 동일하다

#정규화
# 벡터가 여러개있을때 1개의 벡터 크기가 1이되도록 벡터값을 바꾸는것
# L1 정규화 : 특징 벡터 각 성분들의 절대값 합이 1이 되도록, 즉 특징 벡터의 L1 norm이 1이 되도록
# L2 정규화 : 특징 벡터 각 성분들의 제곱 합이 1이 되도록, 즉 특징 벡터의 L2 norm이 1이 되도록

input_data = np.array([[3.1, -1.6, 2.3], [-2.4, 6.5, -4.4], [3.5, 1.1, 2.0]])
l1_normalized_data = preprocessing.normalize(input_data, norm='l1')
l2_normalized_data = preprocessing.normalize(input_data, norm='l2')
print("L1 정규화 데이터 : \n", l1_normalized_data)
print("\nL2 정규화 데이터 : \n", l2_normalized_data)

#카테고리 데이터 인코딩
#입력데이터가 전부 수치이길 원하는데 문자열 형태데이터를 수치로 변환해야 할 필요가 있다

encoder = LabelEncoder()
data = ["a","a","b","c","c"]
#encoder.fit(data) #학습
#encoded_data = encoder.transform(data) # 변환
encoded_data = encoder.fit_transform(data) # 학습과 변환 한번에
print("인코딩 데이터 : ", encoded_data)
labeled_data = encoder.inverse_transform(encoded_data)
print("디코딩 데이터 : ", labeled_data)

#LabelEncoder처럼 카테고리 값을 숫자로 변환하면 숫자의 특성 상 값들 사이에 거리 개념이 존재하게 되어 원 데이터의 의미가 일부 손실되는 경우도 있음
#거리가 없는 형태로 수치 데이터로 바꿀 경우는 OneHotEncoder 클래스를 이용 (각 카테고리 값을 단위 벡터, 즉 하나만 1이고 나머지는 0인 형태로 변환)

encoder = preprocessing.LabelEncoder()
data = ["a","a","b","c","c"]
encoded_data = encoder.fit_transform(data)
encoder = preprocessing.OneHotEncoder()
onehot_encoded_data = encoder.fit_transform(encoded_data.reshape(-1,1))
#인코딩 데이터를 단위벡터표현 여기서 a,b,c3개있으므로 해당되는 원소만 1 나머지는 0으로 표현

print(onehot_encoded_data.toarray())

#tenis 나이브 베이즈

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from IPython.display import display
play_tennis = pd.read_csv("PlayTennis.csv")# 테니스 데이터 로드
number = LabelEncoder() # 문자열 playtennis 데이터 수치변환위한 클래스 인스턴스 생성

# play_tennis 의 각 필드별로 학습한뒤 수치화하여 저장
play_tennis['Outlook'] = number.fit_transform(play_tennis['outlook'])
play_tennis['Temperature'] = number.fit_transform(play_tennis['temp'])
play_tennis['Humidity'] = number.fit_transform(play_tennis['humidity'])
play_tennis['Wind'] = number.fit_transform(play_tennis['windy'])
play_tennis['Play Tennis'] = number.fit_transform(play_tennis['play'])

display(play_tennis)

features = ["Outlook", "Temperature", "Humidity", "Wind"] # 입력필드
target = "Play Tennis" # 출력필드

X = play_tennis[features] # 입력 데이터
y = play_tennis[target] # 출력 데이터

model = GaussianNB()# 학습데이터가 이진값이면 베르누이,빈도수이면 멀티노미안, 그외는 가우시안 모델을 사용한다
model.fit(X,y)# 입력데이터와 출력데이터를 가지고 학습

y_pred=model.predict(X) #입력데이터 X에대한 출력 예측

print(accuracy_score(y, y_pred)) # 예측과 실데 데이터에 대한 정확도 계산

#iris 나이브 베이즈
def download_data(url, dir_name, file_name):
  if not os.path.isdir(dir_name):
	  os.makedirs(dir_name)
  file_path = os.path.join(dir_name,file_name)
  urllib.request.urlretrieve(url, file_path)

download_data("https://www.openml.org/data/get_csv/61/dataset_61_iris.arff", "F:\PycharmProjects\Artificailintelligent", "iris.csv")
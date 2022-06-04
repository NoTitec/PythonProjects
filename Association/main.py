import datetime
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from apyori import apriori
store_data = pd.read_csv("store_data.csv",header=None)

now=datetime.datetime.now()
print(now)

print(store_data.head())#데이터 맨위 5줄 출력
print(len(store_data))#데이터 개수 출력

records = []
for i in range(0, 7501):
    records.append([str(store_data.values[i, j]) for j in range(0, 20)])#1행 str변환하여 list에 넣음

#min_support는 7일 5번이상구매항목으로 35/7500 min_confidence는 20% min_lift는 3
association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
association_result = list(association_rules);#학습결과를 list자료형으로 변환

for item in association_result:#각 규칙의 조합,연관규칙,지지도,신뢰도,향상도 출력
    print(item[0])
    items = [x for x in item[0]]# list comprehension

    print(items[0] + " -> " + items[1])
    print("support = " + str(item[1]))
    print("confidence = " + str(item[2][0][2]))
    print("lift = " + str(item[2][0][3]))
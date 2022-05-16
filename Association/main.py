import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from apyori import apriori
store_data = pd.read_csv("store_data.csv",header=None)
print(store_data.head())
print(len(store_data))

records = []
for i in range(0, 7501):
    records.append([str(store_data.values[i, j]) for j in range(0, 20)])#1행 str변환하여 list에 넣음

association_rules = apriori(records, min_support=0.0045, min_confidence=0.5, min_lift=3, min_length=2)
association_result = list(association_rules);

for item in association_result:
    print(item[0])
    items = [x for x in item[0]]# list comprehension

    print(items[0] + " -> " + items[1])
    print("support = " + str(item[1]))
    print("confidence = " + str(item[2][0][2]))
    print("lift = " + str(item[2][0][3]))
    print()
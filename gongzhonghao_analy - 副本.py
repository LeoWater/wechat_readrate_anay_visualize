
import sys
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import matplotlib as mpl
import numpy as np
import seaborn as sns
from datetime import datetime
from pandas import to_datetime


"""用pandas读取csv文件里的数据，生成二维表，并合并两张表"""
df1 = pd.read_csv('1.csv', delimiter=',', sep='\t', encoding='utf-8')
df2 = pd.read_csv('2.csv', delimiter=',', sep='\t', encoding='utf-8')

print(df1)
print(df2)
df1.info()
df2.info()

#df1.postnum.to_numbric()
#df1.to_datetime(['date'],%y-%m-%d)
#df1['postnum'].astype('int')


cols1 = df1[['postnum', 'readnum', 'title', 'date']]
cols2 = df2[['postnum', 'readnum', 'title', 'date']]
#cols2 = df2.iloc[:, [4, 6, 1, 3]]
df3 = cols1.append(cols2, ignore_index=True)
#df3 = pd.join(cols1, cols2, how='inner', )

#print(cols1.head())
#print(cols2.head())
print(df3)


"""没有实现更改postnum列的149人这类数据为149，更改刷新到dataframe中。"""
"""
for a in df1['postnum']:
    a1 = a[:(len(a)-1)]
    df1.replace(a, a1)
print(df1)
"""
#df1['postnum'].str[0:-2]
"""实现新增一列new，将postnum里的149人等数据改为149"""
"""
df1['new'] = df1['postnum'].str[0:-1].astype(int)
#df_dt = to_datetime(df1.date, format="%y%m%d")
print(df1['new'])
"""

#df1['postnum'] = df1['postnum'].replace('\d+人', '\d', regexp=True)


"""实现更改postnum列的149人这类数据为149，更改刷新到dataframe中。"""
def postnum_int(series):
    postnum = series['postnum']
    postnum_int = int(postnum[0:-1])
    return postnum_int


df3['postnum'] = df3.apply(postnum_int, axis=1)

print(df3)


"""增加阅读率数据"""


def read_rate(series):
    postnum = series['postnum']
    readnum = series['readnum']
    read_rate = readnum / postnum
    return read_rate


df3['read_rate'] = df3.apply(read_rate, axis=1)
print(df3)


"""对dataframe按照postnum从小到大进行排序"""

#df4 = df3.sort_index(axis=0, ascending=True, by='postnum')
df4 = df3.sort_values(axis=0, ascending=True, by='postnum')
print(df4)

"""对dataframe按照read_rate从小到大进行排序"""
df5 = df3.sort_values(axis=0, ascending=True, by='read_rate')
print(df5)

"""删除某一行数据"""
#df5 = df4.drop(axis=0, index=81, inplace=False)
df6 = df4.drop(df4[df4.read_rate > 15].index, inplace=False)
print(df6)
df7 = df5.drop(df5[df5.read_rate > 15].index, inplace=False)
print(df7)
"""将dataframe转化为list"""
"""
dataset = df4.values

list1 = []
for k in dataset:
     for j in k:
         list1.append(j)

#print(df4[0:3])
#print(dataset[0:3])
print(dataset)
#print(dataset.replace('\t', ','))
"""
"""
with open('output.csv', 'w', encoding='utf-8', newline='')as f:
    writer = csv.writer(f)
    writer.writerows(dataset)
"""
"""使用matplotlib生成气泡图,按照postnum排序"""



#v1 = df3.iloc[:]

#sns.scatterplot(x="num", y="read_rate1", data=df4)  s=df5['readnum']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(df6['postnum'], df6['read_rate'], )
ax.set_xlabel('postnum')
ax.set_ylabel('read_rate')
plt.axhline(y=0.08, ls=":", c="red")
plt.axhline(y=0.5, ls=":", c="green")


plt.savefig('readrate1.png', dpi=750, bboxinches='tight')
plt.show()


"""使用matplotlib生成气泡图,按照read_rate排序"""


fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(df7['read_rate'], df7['postnum'], )
ax.set_xlabel('read_rate')
ax.set_ylabel('postnum')
plt.axhline(y=0.08, ls=":", c="red")
plt.axhline(y=0.5, ls=":", c="green")


plt.savefig('readrate2.png', dpi=750, bboxinches='tight')
plt.show()


"""使用seaborn生成气泡图"""


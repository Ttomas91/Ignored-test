from his_from_csv import  history_from_csv as hfc


dbase1=hfc("EURUSD","60")
dbase2=hfc("GBPUSD","60")
dbase3=hfc("AUDUSD","60")
dbase4=hfc("NZDUSD","60")
d="2018.01.14"
t='11:00'
   
l=300
db1=dbase1.get_history(d,t,l,'Open')
db2=dbase2.get_history(d,t,l,"Open")
db3=dbase3.get_history(d,t,l,'Open')
db4=dbase4.get_history(d,t,l,"Open")
'''
print (db1)
print ("-" * 8)
print (db11)
print ("-" * 8)
print (db2)
'''


import numpy as np
import pandas as pd
import statsmodels.api as sm
import patsy as pt
import sklearn.linear_model as lm
from ggplot import *

# загружаем файл с данными
d={'x1':db1,'x2':db2,'x3':db3,'x4':db4,'y':[x*1.2 for x in range(l)]}
df = pd.DataFrame(data=d)
ggplot(aes(x="x1", y="y"), data=df)
#print (df)
# x - таблица с исходными данными факторов (x1, x2, x3)
x = df.iloc[:,:-1]
#print (x)
# y - таблица с исходными данными зависимой переменной
y = df.iloc[:,-1]
#print (y)
skm=lm.LinearRegression()
skm.fit(x,y)
print (skm.intercept_)
print ("-"*8)
print (skm.coef_)

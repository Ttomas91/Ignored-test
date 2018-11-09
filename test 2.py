from his_from_csv import  history_from_csv as hfc

import numpy as np
import pandas as pd
import statsmodels.api as sm
import patsy as pt
import sklearn.linear_model as lm
import os



def OnePointValue(Symbol,lot,dat,tim,tf):
    
    value=1
    if Symbol[-3:]=="USD":
        return 1
    
    elif Symbol[:3]=="USD":
        tmpdba=hfc(Symbol,tf)
        s1=tmpdba.get_history(dat,tim,1,'Close')
        onpoint=0.0001
        if Symbol[-3:]=="JPY" or Symbol[-3:]=="RUB":
            onpoint=0.01
        if Symbol[:3]=="XAG" or Symbol[:3]=="XAU":
            onpoint=0.01
        return (100000*lot*onpoint)/s1[0]
    
    elif Symbol+tf+".csv" in os.listdir(os.getcwd()+"/history"):
        tmpdba=hfc(Symbol,tf)
        s1=tmpdba.get_history(dat,tim,1,'Close')
        onpoint=0.0001
        if Symbol[-3:]=="JPY" or Symbol[-3:]=="RUB":
            onpoint=0.01
        if Symbol[:3]=="XAG" or Symbol[:3]=="XAU":
            onpoint=0.01
        opv=(100000*lot*(s1[0]+onpoint))-(100000*lot*s1[0])
        
        quote=Symbol[-3:]
        if "USD"+quote+tf+".csv" in os.listdir(os.getcwd()+"/history"):
            tmpdba=hfc("USD"+quote,tf)
            s1=tmpdba.get_history(dat,tim,1,'Close')
            opv=opv/s1[0]
        return opv


d="2018.01.14"
t='11:00'   
l=10
timeframe='60'

tradeSym="AUDUSD,EURUSD,GBPUSD,NZDUSD,USDCAD,USDCHF,USDJPY"


Symbols=tradeSym.split(',')

base=[hfc(x,timeframe) for x in Symbols]
dbase=[x.get_history(d,t,l,'Open') for x in base]
rost=[[x-dbase[y][0] for x in dbase[y]] for y in range(len(dbase))]

'''
lots=0.1
db11=db1[:]
for x in range(len(db11)):
    db11[x]=db11[x]-db1[0]
#print (OnePointValue("EURUSD",lots,d,t,"60"))
'''
'''
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
'''

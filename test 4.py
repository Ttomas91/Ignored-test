from his_from_csv import  history_from_csv as hfc

import numpy as np
import pandas as pd
import statsmodels.api as sm
import patsy as pt
import sklearn.linear_model as lm
import os
import itertools

from math import factorial


def toFixed(numObj, digits=0):
    return float(f"{numObj:.{digits}f}")

def calculate_combinations(n, r):
    return int(factorial(n)/factorial(r)/factorial(n-r))

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
inc=20
timeframe='60'

tradeSym="AUDUSD,EURUSD,GBPUSD,NZDUSD,USDCAD,USDCHF,USDJPY"


Symbols=tradeSym.split(',')

base=[hfc(x,timeframe) for x in Symbols]
dbase=[x.get_history(d,t,l,'Open') for x in base]
rost=[[x-dbase[y][0] for x in dbase[y]] for y in range(len(dbase))]

for s in range(len(Symbols)):
    if Symbols[s][:3]=="JPY" or Symbols[s][-3:]=="JPY":
        o=OnePointValue(Symbols[s],1,d,t,timeframe)
        rost[s]=[toFixed(x*100*o,4) for x in rost[s]]
    else:
        o=OnePointValue(Symbols[s],1,d,t,timeframe)
        rost[s]=[toFixed(x*10000*o,4) for x in rost[s]]
 

g=itertools.combinations(range(len(Symbols)), 4 )
for c in range(1):#calculate_combinations(len(Symbols), 4 )):
    d={}
    kou=next(g)
    for e in range(len(kou)):
        d[Symbols[kou[e]]]=rost[kou[e]]
    d['y']=[x*inc for x in range(l)]
    #d={'x1':db1,'x2':db2,'x3':db3,'x4':db4,'y':[x*1.2 for x in range(l)]}
    #print (d)
    
    df = pd.DataFrame(data=d)
    #print (df)

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
    z=[]
    for x in range(l):
        coi=0
        for e in range(len(kou)):
            coi+=d[Symbols[kou[e]]][x]*skm.coef_[e]
        z.append(coi+skm.intercept_)
    d["z"]=z
    df = pd.DataFrame(data=d)
    print (df)

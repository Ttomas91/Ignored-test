from his_from_csv import  history_from_csv as hfc
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import patsy as pt
import sklearn.linear_model as lm
import os
import itertools
from pylab import *
from math import factorial

from pandas import date_range,Series,DataFrame,read_csv, qcut

from numpy.random import randn

def toFixed(numObj, digits=0):
    return float(f"{numObj:.{digits}f}")

def calculate_combinations(n, r):
    return int(factorial(n)/factorial(r)/factorial(n-r))

def OnePointValue(Symbol,lot,dt,tf):

    value=1
    if Symbol[-3:]=="USD":
        return 1
    
    elif Symbol[:3]=="USD":
        tmpdba=hfc(Symbol,tf)
        s1=tmpdba.get_history(dt,1,'Close')
        onpoint=0.0001
        if Symbol[-3:]=="JPY" or Symbol[-3:]=="RUB":
            onpoint=0.01
        if Symbol[:3]=="XAG" or Symbol[:3]=="XAU":
            onpoint=0.01
        return (100000*lot*onpoint)/s1[0]
    
    elif Symbol+tf+".csv" in os.listdir(os.getcwd()+"/history"):
        tmpdba=hfc(Symbol,tf)
        s1=tmpdba.get_history(dt,1,'Close')
        onpoint=0.0001
        if Symbol[-3:]=="JPY" or Symbol[-3:]=="RUB":
            onpoint=0.01
        if Symbol[:3]=="XAG" or Symbol[:3]=="XAU":
            onpoint=0.01
        opv=(100000*lot*(s1[0]+onpoint))-(100000*lot*s1[0])
        
        quote=Symbol[-3:]
        if "USD"+quote+tf+".csv" in os.listdir(os.getcwd()+"/history"):
            tmpdba=hfc("USD"+quote,tf)
            s1=tmpdba.get_history(dt,1,'Close')
            opv=opv/s1[0]
        return opv

def NextIter(sdig,datm):
    date=datm[0].split('.')
    tim=datm[1].split(':')
    if int(tim[0])+int(sdig)<10:
        tim[0]="0"+str(int(tim[0])+int(sdig))
    else:tim[0]=str(int(tim[0])+int(sdig))
    if int(tim[0])>=24:
        power=(int(tim[0])//24)
        print (power)
        if int(tim[0])-24*power <10:
            tim[0]="0"+str(int(tim[0])-24*power)
        else: tim[0]=str(int(tim[0])-24*power)
        if int(date[2])+power<10:
            date[2]="0"+str(int(date[2])+power)
        else:date[2]=str(int(date[2])+power)
        if int(date[2])>28 and int(date[1])==2 and int(date[0])%4!=0:
            if int(date[2])-28<10:
                date[2]="0"+str(int(date[2])-28)
            else:date[2]=str(int(date[2])-28)
            date[1]='03'
        elif int(date[2])>29 and int(date[1])==2 and int(date[0])%4==0:
            if int(date[2])-29<10:
                date[2]="0"+str(int(date[2])-29)
            else:date[2]=str(int(date[2])-29)
            date[1]='03'
        elif int(date[2])>30 and int(date[1]) in [4,6,9,11]:
            if int(date[2])-30<10:
                date[2]="0"+str(int(date[2])-30)
            else:date[2]=str(int(date[2])-30)
            if int(date[1])+1<10:
                date[1]="0"+str(int(date[1])+1)            
            else: date[1]=str(int(date[1])+1)
        elif int(date[2])>31 and int(date[1]) in [1,3,5,7,8,10,12]:
            if int(date[2])-31<10:
                date[2]="0"+str(int(date[2])-31)
            else:date[2]=str(int(date[2])-31)
            if int(date[1])+1<10:
                date[1]="0"+str(int(date[1])+1)            
            else: date[1]=str(int(date[1])+1)
            if int(date[1])>12:
                
                if int(date[1])-12<10:
                    date[1]="0"+str(int(date[1])-12)            
                else: date[1]=str(int(date[1])-12)
                date[0]=str(int(date[0])+1)

    return ['.'.join(date),':'.join(tim)]


        
d="2016.12.30"
t='00:00' 
datatime=[d,t]
le=2
fo=1
inc=10
timeframe='60'

print (datatime)
datatime=NextIter(53,datatime)
'''
print ("-*-"*8)
print (datatime)
k=hfc("EURUSD",timeframe)
g=k.get_history(datatime,le+fo,-1)
print(g)
'''
tradeSym="AUDUSD,EURUSD,GBPUSD,NZDUSD,USDCAD,USDCHF,USDJPY"


Symbols=tradeSym.split(',')

base=[hfc(x,timeframe) for x in Symbols]
dbase=[x.get_history(datatime,le+fo,'Open') for x in base]
rost=[[x-dbase[y][0] for x in dbase[y]] for y in range(len(dbase))]

for s in range(len(Symbols)):
    if Symbols[s][:3]=="JPY" or Symbols[s][-3:]=="JPY":
        o=OnePointValue(Symbols[s],1,datatime,timeframe)
        rost[s]=[toFixed(x*100*o,4) for x in rost[s]]
    else:
        o=OnePointValue(Symbols[s],1,datatime,timeframe)
        rost[s]=[toFixed(x*10000*o,4) for x in rost[s]]
 

g=itertools.combinations(range(len(Symbols)), 4 )
for c in range(1):#calculate_combinations(len(Symbols), 4 )):
    d={}
    kou=next(g)
    for e in range(len(kou)):
        d[Symbols[kou[e]]]=rost[kou[e]]
    d['y']=[x*inc for x in range(le+fo)]
    
    df = pd.DataFrame(data=d)
    x = df.iloc[:le,:-1]
    y = df.iloc[:le,-1]
    
    skm=lm.LinearRegression()
    skm.fit(x,y)
    print (skm.intercept_)
    print ("-"*8)
    print (skm.coef_)
    z=[]
    for x in range(le+fo):
        coi=0
        for e in range(len(kou)):
            coi+=d[Symbols[kou[e]]][x]*skm.coef_[e]
        z.append(coi+skm.intercept_)
    d["z"]=z
    df = pd.DataFrame(data=d)
    '''
    # Визуализация
    print (df)
    df.plot();
    show()
    '''



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

def NormalizeLot(coeff):
    dr=1/sum(abs(coeff))
    return [toFixed(x*dr,2) for x in coeff]
    

portLot=1        
d="2010.01.18"
t='08:00' 
datatime=[d,t]
le=100
fo=50
inc=10
timeframe='60'

'''
datatime=NextIter(53,datatime)

print ("-*-"*8)
print (datatime)
k=hfc("EURUSD",timeframe)
g=k.get_history(datatime,le+fo,-1)
print(g)
'''
tradeSym="AUDUSD,EURUSD,GBPUSD,NZDUSD,USDCAD,USDCHF,USDJPY"


Symbols=tradeSym.split(',')
#print (Symbols.index('NZDUSD'))
base=[hfc(x,timeframe) for x in Symbols]
count_ver_summ=0
count_ver_rost=0
count_ver=0
profit=0
for g in range(100):
    datatime=NextIter(41,datatime)
    print(g,datatime)
    dbase=[x.get_history(datatime,le+fo,'Open') for x in base]
    rost=[[x-dbase[y][0] for x in dbase[y]] for y in range(len(dbase))]

    for s in range(len(Symbols)):
        if Symbols[s][:3]=="JPY" or Symbols[s][-3:]=="JPY":
            o=OnePointValue(Symbols[s],1,datatime,timeframe)
            rost[s]=[toFixed(x*100*o,4) for x in rost[s]]
        else:
            o=OnePointValue(Symbols[s],1,datatime,timeframe)
            rost[s]=[toFixed(x*10000*o,4) for x in rost[s]]
     

    g=itertools.combinations(range(len(Symbols)), 5 )
    tmp_collect_sintetic={}
    tmp_coll_sin=[]
    for c in range(calculate_combinations(len(Symbols), 5 )):
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
        '''
        print ("-"*8)
        print (skm.intercept_)
        print (skm.coef_)
        print ("-"*8)
        print ("n_coeff ",n_coeff)
        print ("-"*8)
        '''
        n_coeff=NormalizeLot(skm.coef_)
        #--------- запоминаем формулу синтетика
        tmp_sin={}
        for e in range(len(kou)):
            tmp_sin[Symbols[kou[e]]]=n_coeff[e]#skm.coef_[e]
        tmp_sin["err"]=skm.intercept_
        #---------
        
        z=[]
        sko=0
        coe_r2_bek=skm.score(x,y)
        x = df.iloc[:,:-1]
        y = df.iloc[:,-1]
        z1 = skm.predict(x)
        coe_r2_summ=skm.score(x,y)
        x = df.iloc[le:,:-1]
        y = df.iloc[le:,-1]
        coe_r2_fow=skm.score(x,y)
        #print ('bec = ',coe_r2_bek,' |  foward = ',coe_r2_fow, " |  Summ = ",coe_r2_summ)
        for x in range(le+fo):
            coi=0
            for e in range(len(kou)):
                coi+=d[Symbols[kou[e]]][x]*n_coeff[e]
            z.append(coi)
            
        
        #for x in range(le+fo):
            #print ("z1 = ",z1[x],'z_orig = ',z[x])
        count_ver+=1
        if coe_r2_bek>0.95:
            count_ver_summ+=1
            profit+=z[le+fo-1]-z[le]
            if z[le+fo-1]-z[le]>0:
                count_ver_rost+=1
        tmp_coll_sin.append(tmp_sin)
        d["z"]=z
        df = pd.DataFrame(data=d)
        '''
        if c==31:
            
            # Визуализация
            print (df)
            df.plot();
            show()
        '''
print ("Всего наблюдаемых синтетиков ", count_ver)
print ("Синтетики с хорошей оптимизацией ", count_ver_summ)
print ("Синтетики которые выросли в фоварде ", count_ver_rost)
print ("% выросших синтетиков из хороших ", toFixed(count_ver_rost/(count_ver_summ/100),2))
print ('Суммарный профит = ',profit)
print ('Мат ожидание = ',profit/count_ver_summ)
collect_sintetic = pd.DataFrame(data=tmp_coll_sin)
#print(collect_sintetic["SKO"])
'''
tmp_collect_sintetic["DT"]=datatime
tmp_collect_sintetic["Len"]=le
tmp_collect_sintetic["Fow"]=fo
tmp_collect_sintetic["Inc"]=inc

tmp_collect_sintetic["Collect"]=tmp_coll_sin
collect_sintetic = pd.Series(data=tmp_collect_sintetic)
print(collect_sintetic["Collect"])
'''



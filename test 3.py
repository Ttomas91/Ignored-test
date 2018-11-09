from his_from_csv import  history_from_csv as hfc

import numpy as np
import pandas as pd
import statsmodels.api as sm
import patsy as pt
import sklearn.linear_model as lm
import itertools

from math import factorial

def calculate_combinations(n, r):
    return int(factorial(n)/factorial(r)/factorial(n-r))

r=[[x*1.2 for x in range(10)] for y in range(7)]
print (len(r))
#print (r)
g=itertools.combinations(range(len(r)), 4 )
for c in range(calculate_combinations(len(r), 4 )):
    print (next(g))
print ("end")

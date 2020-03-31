# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:12:16 2020

@author: HanaFI
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from xbbg import blp

stats.zscore(0.95)

Start = "20150101"
End = pd.to_datetime("today").strftime("%Y%m%d")
df = blp.bdh(tickers= ["CO1 Comdty"],start_date = Start , end_date = End)
df.columns = ["CO"]


Ret = (np.log(df) - np.log(df.shift(1))).dropna()




def VaRCovariance(Ret, ZScore = 1.65, Nominal = 1000):
    '''
    Variance-Covariance Method
    Z Score: 95%: 1.65, 99%: 2.33
    Formula:
    Mean - (zscore * PortStDev) * Nominal
    '''
    pd.DataFrame((ZScore * Ret[-252:].std()), columns = ["VaR %"])
    (ZScore * Ret[-252:].std()) * Nominal

# 5% -> $50


# Historical Simulation
Ret[-1000:].sort_values("CO").iloc[50]

# 2.8% -> $28



# Monte Carlo         TO DO
#np.random.


VaR = {}
Liste = ['BO','C ','CC','CL','CO','CT','FC','GC','HG','HO','JO','KC','KW','LA','LC','LH','LL','LN','LT','LX','NG','PL','QS','S ','SB','SI','SM','W ', 'XB']
for Commo in Liste:
    VaR[Commo] = {}
    for generic in range(1,6):
        df = blp.bdh(tickers= [Commo + str(generic) + " Comdty"],start_date = Start , end_date = End)
        df.columns = ["X"]
        Ret = (np.log(df) - np.log(df.shift(1))).dropna()
        
        VaR[Commo][str(generic) + " Parametric"] = round((ZScore * Ret[-1000:].std())[0],4)
        VaR[Commo][str(generic) + " Historic"] = round(-Ret[-1000:].sort_values("X").iloc[49][0],4)


test = pd.DataFrame(VaR).T




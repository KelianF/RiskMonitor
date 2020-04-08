# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:05:15 2020

@author: Kelian
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from xbbg import blp
import os


def Updatedb(Ticker, Start = "20000101", End = pd.Timestamp.today().strftime("%Y%m%d")):
    print(len(Ticker), type(Ticker), Ticker)
    if Ticker + ".csv" in os.listdir(r"\\10.155.31.149\멀티에셋\Kelian\DATA\COMMO"):   # Folder Location
        #print("Got From DataBase")
        Pointer = pd.read_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\COMMO\\" + Ticker + ".csv", index_col=0)
        if str(Pointer.index.max()) < End:
            Pointer2 = blp.bdh(tickers= [Ticker],start_date = str(Pointer.index.max()) , end_date = End)
            if len(Pointer2[Pointer2.index > str(Pointer.index.max())]) != 0:
                Pointer2 = Pointer2.iloc[1:,:]
                Pointer2.index = Pointer2.index.strftime("%Y%m%d")
                Pointer2.columns = [Ticker]
                Pointer = pd.concat((Pointer, Pointer2), axis = 0)
                Pointer = Pointer[~Pointer.index.duplicated()]
            Pointer.to_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\COMMO\\" + Ticker + ".csv", index=True)
                
        return Pointer
    else: # Twice
        Pointer = blp.bdh(tickers= [Ticker],start_date = Start , end_date = End)
        Pointer.index = Pointer.index.strftime("%Y%m%d")
        Pointer.columns = [Ticker]
        Pointer.to_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\COMMO\\" + Ticker + ".csv", index=True)
        return Pointer




Commos = ['BO',
 'C ',
 'CC',
 'CL',
 'CO',
 'CT',
 'FC',
 'GC',
 'HG',
 'HO',
 'JO',
 'KC',
 'KW',
 'LA',
 'LC',
 'LH',
 'LL',
 'LN',
 'LT',
 'LX',
 'NG',
 'PL', # Here pb
 'QS',
 'S ',
 'SB',
 'SI',
 'SM',
 'W ', # Here no 8
 'XB',
 "CPI",
 "RS",
 "IJ",
 "CA",
 "QW",
 "KO",
 "ZRR", # Here pb
 "ROC",
 "IOE",
"AC", # Here pb
"PAL",
"AE",
"TRC"
 ]



for x in Commos:
    for Futures in range(1,9):
        if x in ["PL", "W ", "ZRR", "AC"] and Futures > 5 :
            continue
        else:
            Updatedb(x + str(Futures) + " Comdty")
        
        
        
        
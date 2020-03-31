# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:02:56 2020

@author: HanaFI
"""

import os

import pandas as pd
import numpy as np

def GetData():
    df = None
    for x in os.listdir(r"\\10.155.31.149\멀티에셋\Kelian\DATA\COMMO\\"):
        if df is None:
            df = pd.read_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\COMMO\\" + x, index_col =0)
        else:
            df = pd.concat((df, pd.read_csv(r"\\10.155.31.149\멀티에셋\Kelian\DATA\COMMO\\" + x, index_col =0)), axis = 1)
    df.columns = [' '.join(x.split(" ")[:-1]) for x in df.columns]
    return df




def VaRCovariance(Ret, ZScore = 1.65, Nominal = 1000):
    '''
    Variance-Covariance Method
    Z Score: 95%: 1.65, 99%: 2.33
    Formula:
    Mean - (zscore * PortStDev) * Nominal
    '''
    VaRdf = pd.DataFrame((100 * ZScore * Ret[-252:].std()), columns = ["VaR %"]) 
    VaRdf = pd.concat((VaRdf, pd.DataFrame((ZScore * Ret[-252:].std()) * Nominal, columns = ["VaR Nom."])), axis = 1)
    return round(VaRdf ,2)

def NormalizePrice(Ret):
    Ret.sort_index()
    Ret = Ret + 1
    Ret.iloc[0] = 100
    Ret = Ret.cumprod()
    Ret = pd.DataFrame(Ret)
    return round(Ret, 2)

def MDD(Ret, Method = "Points"):   
    
    Price = NormalizePrice(Ret)
    Price["Max"] = 100.0
    for x in range(1, len(Price)):
        Price.iloc[x,1] = max(Price.iloc[x-1,1], Price.iloc[x,0])
    Price["Diff"] = Price.Max - Price.iloc[:,0]
    Price["Perct"] = 0
    
    Base = Price.iloc[0,0]
    for x in range(len(Price)):
        if Price.iloc[x,2] == 0.0:
            Base = Price.iloc[x,0]
        Price.iloc[x,3] = Price.iloc[x,0] / Base - 1
    
    if Method[:3] == "Poi":
        return round(max(Price.Diff),2)
    elif Method[:3] == "Per":
        return round(100 * min(Price.Perct), 2)
    elif Method[:3] == "Dat":
        return pd.to_datetime(Price[Price.Diff == max(Price.Diff)].index[0]).strftime("%Y-%m-%d")
    else:
        return Price


def MDDdf(Ret):
    MDDDico = {}
    for x in Ret.columns:
        MDDDico[x] = {}    
        MDDDico[x]["MDD Points"] = MDD(Ret[x], Method = "Points")
        MDDDico[x]["MDD %"] = MDD(Ret[x], Method = "Percentage")
        MDDDico[x]["MDD Dates"] = MDD(Ret[x], Method = "Date") #.astype(str)
    return pd.DataFrame(MDDDico).T

def MDD1_5D(Ret):
    MDDDico = {}
    for x in Ret.columns:
        MDDDico[x] = {}
        MDDDico[x]["MDD 1D"] = Ret[x].min()
        MDDDico[x]["MDD 2D"] = Ret[x].rolling(2).sum().min()
        MDDDico[x]["MDD 5D"] = Ret[x].rolling(5).sum().min()
        
        MDDDico[x]["MDD 1D 1Y"] = Ret[x][-252:].min()
        MDDDico[x]["MDD 2D 1Y"] = Ret[x][-252:].rolling(2).sum().min()
        MDDDico[x]["MDD 5D 1Y"] = Ret[x][-252:].rolling(5).sum().min()
    return round(pd.DataFrame(MDDDico).T, 2)
        
def BasicStats(Ret):
    MDDDico = {}
    for x in Ret.columns:
        MDDDico[x] = {}
        MDDDico[x]["Mean"] = 100 * Ret[x].mean()
        MDDDico[x]["Std"] = np.sqrt(252) * Ret[x].std()
        MDDDico[x]["Skewness"] = Ret[x].skew()
        MDDDico[x]["Kurtosis"] = Ret[x].kurt()
        
        MDDDico[x]["Mean 1Y"] = 100 * Ret[x][-252:].mean()
        MDDDico[x]["Std 1Y"] = np.sqrt(252) * Ret[x][-252:].std()
        MDDDico[x]["Skewness 1Y"] = Ret[x][-252:].skew()
        MDDDico[x]["Kurtosis 1Y"] = Ret[x][-252:].kurt()
    return round(pd.DataFrame(MDDDico).T, 2)

def SecondOrderMetrics(df, Ret):
    df["Calmar"] = 100 * df["Mean"] / df["VaR %"]
    df["MDD/Std"] = (df["MDD %"] / df["Std"]).astype(float)
    return round(df, 2)

def Returns(Selection = False):
    df = GetData().dropna()
    if Selection == True:
        MainOnes = ['BO', 'C ', 'CC', 'CL', 'CO', 'CT', 'FC', 'GC', 'HG', 'HO', 'JO', 'KC', 'KW', 'LA', 'LC', 'LH', 'LL', 'LN', 'LT', 'LX', 'NG', 'PL', 'QS', 'S ', 'SB', 'SI', 'SM', 'W ','XB']
        df = df[[x for x in df.columns if x[:2] in MainOnes]]
    elif Selection == "Quick":
        MainOnes = ['BO', 'C ', 'CC', 'CL', 'CO']
        df = df[[x for x in df.columns if x[:2] in MainOnes]]
    return (np.log(df) - np.log(df.shift(1))).dropna()

def main():
    Ret = Returns(Selection = "Quick")
    if pd.to_datetime("now").strftime("%Y%m%d%p") + ".csv" == max(os.listdir(r"\\10.155.31.149\멀티에셋\Kelian\Risk\\")):
        df = pd.read_csv(r"\\10.155.31.149\멀티에셋\Kelian\Risk\\" + max(os.listdir(r"\\10.155.31.149\멀티에셋\Kelian\Risk\\")), index_col = 0)
    else:
        print("Long part")
        df = pd.concat((BasicStats(Ret), MDDdf(Ret), MDD1_5D(Ret), VaRCovariance(Ret) ), axis=1).reset_index()
        df = SecondOrderMetrics(df, Ret)
        df.to_csv( r"\\10.155.31.149\멀티에셋\Kelian\Risk/" + pd.to_datetime("now").strftime("%Y%m%d%p") + ".csv")
    return df

 
 







#['BO', 'C ', 'CC', 'CL', 'CO', 'CT', 'FC', 'GC', 'HG', 'HO', 'JO', 'KC', 'KW', 'LA', 'LC', 'LH', 'LL', 'LN', 'LT', 'LX', 'NG', 'PL', 'QS', 'S ', 'SB', 'SI', 'SM', 'W ','XB']








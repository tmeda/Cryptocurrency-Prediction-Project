import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

def ac_pac(df,lags):
    row=len(df.columns)
    fig, ax = plt.subplots(row,2,figsize=(12,16))
    ind=0
    fig.tight_layout(h_pad=2, w_pad=2)
    for r in range(row):
        col=df.columns[ind]
        plot_acf(df[col], lags = lags,ax=ax[r][0])
        ax[r][0].set_title(col+' Autocorrelation')

        plot_pacf(df[col], lags = lags,ax=ax[r][1])
        ax[r][1].set_title(col+' Partial Autocorrelation')
        ind+=1
def plot_indexes(df):
    plt.figure(figsize=(16,8))
    plt.xlabel('Date')
    plt.ylabel('Price')
    for i in df.columns:
        plt.plot(df.index,df[i],label=i,linewidth=6)
        plt.legend()
def plot_linear_relationships(df):
    y=['bit_close','eth_close','ada_close','bnb_close']
    y=df[y]
    rows=len(y.columns)
    final=[]
    for row in range(rows):
        temp1=df.corr()[y.columns[row]]
        temp1=pd.DataFrame(temp1).T.drop(columns=y.columns)
        temp1=temp1.T.dropna()
        temp1=(temp1**2)**0.5

        x=temp1[(temp1[y.columns[row]])>0.5].index
        final+=list(x)
        x=df[x]
        columns=len(x.columns)

        fig, ax = plt.subplots(1,columns,figsize=(20,4))
        fig.suptitle(t=f'Variables plotted against {y.columns[row]}', size=20)
        fig.tight_layout(h_pad=1.5, w_pad=1.5)
        corrector=0
        for column in range(columns):
            if (x.columns[column])==(y.columns[row]):
                corrector=1
            ax[column].scatter(x[x.columns[column+corrector]],y[y.columns[row]],alpha=0.6)
            ax[column].set_title(x.columns[column+corrector]+' v.s. '+ y.columns[row])
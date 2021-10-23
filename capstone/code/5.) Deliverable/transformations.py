import numpy as np
import pandas as pd
import pickle

def arima_data(df):
    return np.log(df).diff(1).dropna()
    
def linear_model_1(df):   
    features={'BNB-USD':0,'ETH-USD':0,'ADA-USD':0,'BTC-USD':0}
    targets=['BNB-USD','ETH-USD','ADA-USD','BTC-USD']
    for target in targets:
        y=pd.DataFrame(df[target])
        for lags in range(1,100):
            y[f'lag_{lags}']=y[target].shift(lags)
        features[target]=y.dropna()
    return features

def linear_model_2(df): 
    data={}
    targets=['BNB-USD','ETH-USD','ADA-USD','BTC-USD']
    for target in targets:
        x=df.drop(columns=target)
        y=df[target]
        temp=pd.DataFrame()
        for col in x.columns:
            for i in range(2,10):
                temp[f'{col}**{i}']=x[col]**i
        temp[target]=y
        temp1=pd.DataFrame(temp.corr()[target])
        temp1=temp1.sort_values(by=target,ascending=False)
        temp1=temp1[(temp1[target]>=0.5) & (temp1[target]<1)]
        res=[]
        for cols in x.columns:
            ind=0
            while ind<len(temp1.index):
                if str(cols) in list(temp1.index)[ind]:
                    res.append(list(temp1.index)[ind])
                    cols=len(temp1.index)
                else:
                    ind+=1
        temp=temp[res]
        temp=pd.DataFrame(temp, columns=temp.columns)
        x=x.merge(temp,on=x.index)
        x.drop(columns='key_0',inplace=True)
        x=x.dropna()
        data[target]=x
    for i,j in data.items():       
        for k in range(1,11):
            j['day_'+str(k)]=df[i].shift(-k).values
        data[i]=j.dropna()   

    with open('../../data/train/inear_log(price_data).pkl', 'wb') as f:
        pickle.dump(data,f)
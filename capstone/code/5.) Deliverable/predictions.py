def predict():
    import yfinance as yf
    import models
    import pandas as pd
    import transformations
    from sklearn.model_selection import train_test_split
    import matplotlib.pyplot as plt
    import numpy as np
    #https://pypi.org/project/yfinance/
    msft = yf.Ticker("MSFT")
    hist = msft.history(period="5")
    df=pd.DataFrame()
    for i in ['BNB-USD','ETH-USD','ADA-USD','BTC-USD','DJI','NVDA','AMD','^IXIC','^GSPC']: 
        temp = yf.Ticker(i).history(period="max")['Close']
        df[i]=temp
    df=df.dropna()


    #perform feature engineering
    arima=transformations.arima_data(df)
    lin_mod_1=transformations.linear_model_1(df)
    transformations.linear_model_2(df)
    preds=pd.DataFrame()
    preds2=pd.DataFrame()

    targets=['BNB-USD','ETH-USD','ADA-USD','BTC-USD']

    #predict future prices
    preds1=models.linear_model_1(lin_mod_1,preds)
    preds1=models.monte(df,preds,targets)
    preds1=models.linear_model_2(preds)
    preds2=models.multi_arima(arima,targets)
    preds2=models.uni_arima(arima,preds2,targets)

    #display predictions

    row=len(targets)
    fig, ax = plt.subplots(row,2,figsize=(12,16))
    ind=0
    fig.tight_layout(h_pad=2, w_pad=2)

    for r in range(row):
        col=targets[ind]
        temp=[i for i in preds1.columns if col in i]
        tar=np.log(df[col]).diff(1).dropna()
        nul=pd.DataFrame([df[col].mean() for i in range(10)],index=tar.index[-10:])


        ax[r][0].plot(preds1[temp[0]],label=temp[0])
        ax[r][0].plot(preds1[temp[1]],label=temp[1])
        ax[r][0].plot(preds1[temp[2]],label=temp[2])
        ax[r][0].plot(nul,label='null model',marker='o')
        ax[r][0].plot((df[col][-10:]),label=col,marker='D')
        ax[r][0].set_title(col+' Prices')
        ax[r][0].legend()


        temp=[i for i in preds2.columns if col in i]
        nul=pd.DataFrame([tar.mean() for i in range(10)],index=tar.index[-10:])
        ax[r][1].plot(preds2[temp[0]],label=temp[0])
        ax[r][1].plot(preds2[temp[1]],label=temp[1])
        ax[r][1].plot(nul,label='null model',marker='o')
        ax[r][1].plot((tar[-10:]),label=col,marker='D')
        ax[r][1].set_title(f'log({col}) Price Change')
        ax[r][1].legend()
        ind+=1
    return (fig,ax)

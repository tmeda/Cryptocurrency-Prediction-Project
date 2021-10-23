from sklearn.linear_model import Ridge
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")
import pickle

def linear_model_1(df,preds):
    for i,j in df.items():
        x=j.drop(columns=[i])
        x=sm.add_constant(x)
        y=j[i]
        X_train, X_test, y_train, y_test = train_test_split(x,y,test_size = 0.011,shuffle = False)
        model= Ridge(fit_intercept=False)
        model.fit(X_train, y_train)
        preds[i+'_lin_model']=model.predict(X_test)
    preds.index=X_test.index
    return preds

def monte(df,preds,targets):  
    train, test = train_test_split(df,test_size = 0.011,shuffle = False)
    for target in targets: 
        prices=np.log(df[target])
        change=((prices-prices.shift(1))/prices).dropna()
        days=10
        simulations=[]
        rmses=[]
        for run in range(100):
            predictions=[prices[-1]]
            for day in range(days):
                predictions.append(predictions[-1]*(1+np.random.choice(change)))
            simulations.append(predictions[1:-1])
        simulations=pd.DataFrame(simulations)
        preds[target+'_monte_carlo']=np.exp(simulations.mean().values)
    return preds

def uni_arima(df,preds,targets):
    for column in targets:
        data=df[column]
        train, test = train_test_split(data,test_size = 0.011,shuffle = False)
        #https://stackoverflow.com/questions/58510659/error-valuewarning-a-date-index-has-been-provided-but-it-has-no-associated-fr/58511282
        train.index = pd.DatetimeIndex(train.index).to_period('D')
        test.index = pd.DatetimeIndex(test.index).to_period('D')

        best_aic = 99 * (10 ** 16)
        best_p = 0
        best_q = 0

        # Use nested for loop to iterate over values of p and q.
        for p in range(5):
            for q in range(5):
                # Insert try and except statements.
                try:
                    # Instantiate ARIMA model.
                    arima = ARIMA(endog = train, # endog = y - variable
                                 order = (p, 1, q)) # values of p, d, q

                    # Fit ARIMA model.
                    model = arima.fit()

                    # Is my current model's AIC better than our best_aic?
                    if model.aic < best_aic:
                        # If so, let's overwrite best_aic, best_p, and best_q.
                        best_aic = model.aic
                        best_p = p
                        best_q = q

                except:
                    pass
        model = ARIMA(endog = train,
                     order = (best_p, 1, best_q))

        # Fit ARIMA model.
        arima = model.fit()

        # Generate predictions based on test set.
        predictions = model.predict(params = arima.params,
                             start = test.index[0],
                             end = test.index[-1])
        col=column+'_uni_arima'
        preds[col]=predictions[:9]
    return preds
        
def multi_arima(df,targets):
    from statsmodels.tsa.vector_ar.var_model import VAR
    #run multi-arima
    train, test = train_test_split(df,test_size = 0.011,shuffle = False)


    model = VAR(endog=train.values)
    model_fit = model.fit()

    # make prediction on validation
    prediction = model_fit.forecast(model_fit.y, steps=len(test))
    pred=pd.DataFrame(prediction,columns=test.columns,index=test.index)
    pred=pred[targets]
    

    pred.columns=[i+'_multi_arima' for i in pred.columns]

    return pred[:9]

def linear_model_2(preds):
    with open('../../data/train/inear_log(price_data).pkl', 'rb') as f:
        data=pickle.load(f)

    targets=['BNB-USD','ETH-USD','ADA-USD','BTC-USD']
    for target in targets:
        ys=[i for i in data[target].columns if 'day' in i]
        x=data[target].drop(columns=ys)
        temp=[]
        for i in ys:
            x=sm.add_constant(x)
            y=data[target][i]
            X_train, X_test, y_train, y_test = train_test_split(x,y,test_size = 1,shuffle = False)
            model= Ridge(fit_intercept=False)
            model.fit(X_train, y_train)
            temp.append(model.predict(X_test)[0])
        preds[target+'multi_lin']=temp[:-1]
    return preds
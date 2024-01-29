from prophet import Prophet
import yfinance as yf
import pandas as pd
import numpy as np


def predict(ticker: str):

    # get the data
    company = yf.Ticker(ticker)
    data = company.history('5y')
    data.reset_index(inplace=True)
    
    # if no data return empty object
    if(len(data) == 0):
        return 'No data' 
    
    # create prophet obj
    prophet = Prophet()

    # Remove timezone from date column
    data['Date'] = data['Date'].apply(lambda date: date.replace(tzinfo=None))

    # replace the header, date to 'ds' and column to analyze to 'y'
    data.columns = [ 'ds', 'y','High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']

    # fit the data
    prophet.fit(df=data)

    # make a future df of 30 days, which will add next 30 dates from ending of the df
    future = prophet.make_future_dataframe(periods=30)
    
    # make predictions
    forecast = prophet.predict(future)
    
    # get 6 months of data and forecast data
    data = data[-130:][['ds', 'y']] if len(data) >=130 else data[['ds', 'y']]
    prediction = forecast[-30:][['ds', 'yhat']]

    # merge them into 1 df
    result = pd.concat([data, prediction])

    # rename the cols
    result.columns = ['date', 'past', 'forecast']

    # replace nan with none
    result = result.replace({np.nan: None})

    # return output as array of objects
    return result.to_dict(orient='records')

    

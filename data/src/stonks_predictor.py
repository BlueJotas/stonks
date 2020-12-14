import math
import numpy as np
import pandas as pd
import investpy
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import datetime
import os


def predictor(ticker):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday_str = datetime.date.strftime(yesterday, "%d/%m/%Y")

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, '../output/tech_data.csv')
    tech_data = pd.read_csv(my_file)
    ipo = tech_data.loc[tech_data['ticker'] == ticker, 'ipo'].iloc[0]
    ipo_str = f'{ipo[-2:]}/{ipo[-5:-3]}/{ipo[:4]}'

    df = investpy.get_stock_historical_data(stock='AAPL', country='united states', as_json=False, order='ascending', from_date=ipo_str, to_date=yesterday_str)

    #Create a new dataframe with only the 'Close' column
    data = df.filter(['Close'])
    #Converting the dataframe to a numpy array
    dataset = data.values
    #Get /Compute the number of rows to train the model on
    training_data_len = math.ceil(len(dataset)*0.8)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    #Create the scaled training data set
    train_data = scaled_data[0:training_data_len  , : ]
    #Split the data into x_train and y_train data sets
    x_train=[]
    y_train = []
    for i in range(60,len(train_data)):
        x_train.append(train_data[i - 60:i,0])
        y_train.append(train_data[i,0])

    #Convert x_train and y_train to numpy arrays
    x_train, y_train = np.array(x_train), np.array(y_train)

    #Reshape the data into the shape accepted by the LSTM
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

    #Build the LSTM network model
    model = Sequential()
    model.add(LSTM(units=24, return_sequences=True,input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=24, return_sequences=False))
    model.add(Dense(units=12))
    model.add(Dense(units=1))

    #Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    #Train the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    #Test data set
    test_data = scaled_data[training_data_len - 60: , : ]
    #Create the x_test and y_test data sets
    x_test = []
    y_test =  dataset[training_data_len : , : ] #Get all of the rows from index 1603 to the rest and all of the columns (in this case it's only column 'Close'), so 2003 - 1603 = 400 rows of data
    for i in range(60,len(test_data)):
        x_test.append(test_data[i - 60:i,0])

    #Convert x_test to a numpy array
    x_test = np.array(x_test)

    #Reshape the data into the shape accepted by the LSTM
    x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

    #Getting the models predicted price values
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)#Undo scaling

    #Calculate/Get the value of RMSE
    rmse=np.sqrt(np.mean(((predictions - y_test)**2)))

    #Plot/Create the data for the graph
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions

    #Get the quote
    apple_quote = investpy.get_stock_historical_data(stock='AAPL', country='united states', as_json=False, order='ascending', from_date='01/01/2012', to_date='12/12/2020')
    #Create a new dataframe
    new_df = apple_quote.filter(['Close'])
    #Get teh last 60 day closing price
    last_60_days = new_df[-60:].values
    #Scale the data to be values between 0 and 1
    last_60_days_scaled = scaler.transform(last_60_days)
    #Create an empty list
    X_test = []
    #Append teh past 60 days
    X_test.append(last_60_days_scaled)
    #Convert the X_test data set to a numpy array
    X_test = np.array(X_test)
    #Reshape the data
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    #Get the predicted scaled price
    pred_price = model.predict(X_test)
    #undo the scaling
    pred_price = scaler.inverse_transform(pred_price)
    print(pred_price)

predictor('AAPL')

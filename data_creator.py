import pandas as pd
import investpy
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import datetime
import os

# Seaborn global style.
sns.set_context('poster')
sns.set(rc={'figure.figsize': (10, 5), 'xtick.labelsize': 10})
sns.set_style('darkgrid')
sns.set_palette("husl", 9)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, './data/output/tech_data.csv')
tech_data = pd.read_csv(my_file)

def check_ticker():
    # This will convert the name to the ticker in case the user does not know the exact input. Will be later used as input debugging in another function.
    print(" The current default stocks are: apple, amazon, tesla, dropbox and microsoft")
    while 1:
        name = input('Introduce the company name or ticker: ')
        for company in tech_data['name']:
            if name.lower() in company.lower():
                return tech_data.loc[tech_data['name'] == company, 'ticker'].iloc[0]
        print('The name you selected was not found, try again and check if you wrote it correctly.')

def data_model(ticker):
    today = datetime.datetime.now()
    today_str = datetime.date.strftime(today, "%d/%m/%Y")
    from_date = datetime.datetime.now() - datetime.timedelta(days=365)
    from_date_str = datetime.date.strftime(from_date, "%d/%m/%Y")

    data = investpy.get_stock_historical_data(stock=ticker, country='united states', as_json=False, order='ascending', from_date=from_date_str, to_date=today_str)
    close = data['Close']
    delta = close.diff()

    # Make the positive gains (up) and negative gains (down) Series.
    # This is done by converting all the negative values in 'up' to zero and the same thing in down with the positives.
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    window_length = 14

    # Calculate the EWMA.
    avg_gain1 = up.ewm(span=window_length).mean()
    avg_loss1 = down.abs().ewm(span=window_length).mean()

    # Calculate the RSI based on EWMA.
    RS1 = avg_gain1 / avg_loss1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    # Calculate the EWMA for the prices:
    ewma = close.ewm(span=7).mean()

    # Create the test prediction dataframe:
    df_1 = pd.DataFrame({'EWMA':ewma.values})
    df_2 = pd.DataFrame({'RSI':RSI1.values})
    to_pred = {'RSI': [df_2['RSI'].iloc[-1]], 'EWMA': [df_1['EWMA'].iloc[-1]]}
    p = pd.DataFrame(data=to_pred)


    #Create a dataframe with the EWMA price:
    df_1 = pd.DataFrame({'EWMA':ewma.values}).shift(1)

    # Create a dataframe with the RSI:
    df_2 = pd.DataFrame({'RSI':RSI1.values}).shift(1)

    # Create a dataframe with the prices:
    df_3 = pd.DataFrame({'Date':close.index, 'Price':close.values})

    # Loop in order to create a dataframe with the stock name:
    ticker_list = [ticker for i in range(len(close))]
    df_4 = pd.DataFrame({'Stock': ticker_list})
    # Create the ultimate DataFrame:
    frames = [df_2, df_1, df_3, df_4]
    df = pd.concat(frames, axis=1)

    # Dropping first two columns:
    df.drop([0, 1, 2, 3], inplace=True)

    # # Plot graphs:
    # fig, axs = plt.subplots(2)
    # fig.suptitle('Close price (+ EWMA) and RSI')
    # axs[0].plot(close, color='b')
    # axs[0].plot(ewma, color='g')
    # axs[1].plot(RSI1, color='orange')
    # axs[1].axhline(70, 0, color='r')
    # axs[1].axhline(30, 0, color='g')
    # plt.show()

    return df, p

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


def get_data(*args):
    for arg in args:
        stock = investpy.get_stock_historical_data(stock=f'{arg}', country='united states', as_json=False, order='ascending', from_date='01/01/2020', to_date='01/12/2020')
        sns.lineplot(data=stock, x='Date', y='Close', label=arg)

    plt.legend(loc="upper left")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Recent stock data:")
    plt.show()


def get_all_data(): # Do not execute under any circumstances.
    for ticker in tickers:
        try:
            stock = investpy.get_stock_historical_data(stock=f'{ticker}', country='united states', as_json=False, order='ascending', from_date='01/01/2020', to_date='01/12/2020')
            sns.lineplot(data=stock, x='Date', y='Close', label=ticker)
        except Exception:
            continue

    plt.legend(loc="upper left")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Recent stock data:")
    plt.show()


def check_ticker():
    # This will convert the name to the ticker in case the user does not know the exact input. Will be later used as input debugging in another function.
    while 1:
        name = input('Introduce the company name or ticker: ')
        for company in tech_data['name']:
            if name.lower() in company.lower():
                return tech_data.loc[tech_data['name'] == company, 'ticker'].iloc[0]
        print('The name you selected was not found, try again and check if you wrote it correctly.')

def get_rsi(ticker, mode='SMA'):
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

    if mode == 'EWMA':
        # Calculate the EWMA.
        avg_gain1 = up.ewm(span=window_length).mean()
        avg_loss1 = down.abs().ewm(span=window_length).mean()

        # Calculate the RSI based on EWMA.
        RS1 = avg_gain1 / avg_loss1
        RSI1 = 100.0 - (100.0 / (1.0 + RS1))

        # Calculate the EWMA for the prices:
        ewma = close.ewm(span=7).mean()
        df_1 = pd.DataFrame({'EWMA':ewma.values})

        # Create a dataframe with the RSI:
        df_2 = pd.DataFrame({'Date':RSI1.index, 'RSI':RSI1.values})

        # Create a dataframe with the prices:
        df_3 = pd.DataFrame({'Price':close.values})

        # Create the ultimate DataFrame:
        frames = [df_2, df_1, df_3]
        df = pd.concat(frames, axis=1)

        # Plot graphs:
        fig, axs = plt.subplots(2)
        fig.suptitle('Close price (+ EWMA) and RSI')
        axs[0].plot(close, color='b')
        axs[0].plot(ewma, color='g')
        axs[1].plot(RSI1, color='orange')
        axs[1].axhline(70, 0, color='r')
        axs[1].axhline(30, 0, color='g')
        plt.show()


        # RSI1.plot(color='r')
        # plt.axhline(y=70, color='r', linestyle='-', alpha=0.7)
        # plt.axhline(y=30, color='g', linestyle='-', alpha=0.7)
        # plt.show()
        #
        # close.plot(color='b')
        # ewma.plot(color='g')

    else:
        # Calculate the SMA.
        avg_gain2 = up.rolling(window_length).mean()
        avg_loss2 = down.abs().rolling(window_length).mean()

        # Calculate the RSI based on SMA.
        RS2 = avg_gain2 / avg_loss2
        RSI2 = 100.0 - (100.0 / (1.0 + RS2))

        # Plot graph.
        RSI2.plot(color='b')
        plt.axhline(y=70, color='r', linestyle='-', alpha=0.7)
        plt.axhline(y=30, color='g', linestyle='-', alpha=0.7)
        plt.legend(['RSI (SMA)'])
        plt.show()




# TODO: scatter plot for linear regression.

def main():
    ticker = check_ticker()
    while 1:
        mode = input('Select SMA or EWMA: ').upper()
        if mode == 'SMA' or mode == 'EWMA':
            break
    get_rsi(ticker, mode)

main()

from data_creator import check_ticker, data_model
from stonks_predictor import predictor

def main():
    ticker = check_ticker()
    df, p = data_model(ticker)
    predictor(df, p, ticker)

main()

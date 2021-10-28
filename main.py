import json
import time

import pandas_datareader as pdr
import datetime as dt
import matplotlib as mpl
from matplotlib import style, pyplot
from get_all_tickers import get_tickers as gt


def main():
    # uses code from Github *not* from the pip package
    # tickers = gt.get_tickers()
    tickers = ["A", "AA", "AAPL", "MSFT", "TSLA", "AMZN", "YOKEY", "HLMA.L"]

    data_list = get_data_list(tickers)
    create_chart(data_list)
    save_data(data_list)


def get_data_list(tickers):
    start = dt.datetime(1970, 1, 1)
    end = dt.datetime(2021, 12, 31)

    result = {}
    count = 0
    ticker_count = len(tickers)
    for ticker in tickers:
        count += 1
        print(f'Requesting financial data for: {ticker} - {count} / {ticker_count}')
        try:
            data = pdr.get_data_yahoo(ticker, start, end)
            result[ticker] = data
            time.sleep(1)
        except Exception as e:
            print(e)
            print(f'Unable to fetch: {ticker}')

    return result


def create_chart(data_list):
    for k, v in data_list.items():
        plot_trend(v, k)

    pyplot.savefig(f'data/plot.png')


def plot_trend(data, ticker):
    close_px = data['Adj Close']
    rolling_mean = close_px.rolling(window=100).mean()
    mpl.rc('figure', figsize=(20, 15))
    mpl.style.use('ggplot')
    rolling_mean.plot(label=f'{ticker} value')
    pyplot.legend()


def save_data(data_list):
    stock_list = {}
    for k, v in data_list.items():
        data_json = v.to_json()
        stock_list[k] = json.loads(data_json)

    print('Saving data')
    with open(f"data/stock_data.json", "w") as file:
        file.write(json.dumps(stock_list, indent=4))


if __name__ == '__main__':
    main()

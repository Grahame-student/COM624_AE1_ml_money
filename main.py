import json
from time import sleep

import pandas as pd
import pandas_datareader as pdr
import datetime as dt


def main():
    stock_list = {}
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2020, 12, 31)
    tickers = ["AAPL", "MSFT"]
    for ticker in tickers:
        data = pdr.get_data_yahoo(ticker, start, end)
        data_json = data.to_json()
        stock_list[ticker] = json.loads(data_json)

    with open(f"data/stock_data.json", "w") as file:
        file.write(json.dumps(stock_list))


if __name__ == '__main__':
    main()

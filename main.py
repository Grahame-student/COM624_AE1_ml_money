import json
import time
import sys

import pandas_datareader.data as pdr
from PyQt5 import QtWidgets
from pandas.plotting import scatter_matrix
import datetime as dt
import matplotlib as mpl
from matplotlib import style, pyplot
import numpy as np

from financial_model import FinancialModel
from main_controller import MainController
from main_view import UiMainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(main_window)
    controller = MainController(ui, FinancialModel())
    main_window.show()
    sys.exit(app.exec_())

    # uses code from Github *not* from the pip package
    # tickers = gt.get_tickers()
    # tickers = ["A", "AA", "AAPL", "MSFT", "TSLA", "AMZN", "YOKEY", "HLMA.L"]
    tickers = ["HLMA.L"]
    data_list = get_data_list(tickers)
    show_correlations(data_list)
    show_scatters(data_list)
    create_chart(data_list)
    save_data(data_list)


def get_data_list(tickers):
    start = dt.datetime(1970, 1, 1)
    end = dt.datetime(2021, 12, 31)

    result = {}
    count = 0
    profit_shift = 20  # Can pass in as hyper param via GUI front end
    ticker_count = len(tickers)
    for ticker in tickers:
        count += 1
        print(f'Requesting financial data for: {ticker} - {count} / {ticker_count}')
        try:
            data = pdr.get_data_yahoo(ticker, start, end)
            # data[f'symbol'] = ticker
            # data[f'profit'] = data.Low - data.High.shift(profit_shift)
            print(data.head(5))
            result[ticker] = data
            time.sleep(1)
        except Exception as e:
            print(str(e))
            print(f'Unable to fetch: {ticker}')
    return result


def show_correlations(data_list):
    for k, v in data_list.items():
        show_correlation(k, v)


def show_correlation(ticker, data):
    print(f'Calculating correlations for {ticker}')
    df = ((data-data.min()) / (data.max() - data.min()))
    headers = df.columns
    data_correlations = df.corr()

    corr_fig = pyplot.figure()
    axes = corr_fig.add_subplot(111)
    ax_corr = axes.matshow(data_correlations, vmin=-1, vmax=1)
    corr_fig.colorbar(ax_corr)
    ticks = np.arange(0, len(headers), 1)

    axes.set_xticks(ticks)
    axes.set_yticks(ticks)
    axes.set_xticklabels(headers)
    axes.set_yticklabels(headers)

    pyplot.savefig(f'data/corr_{ticker}.png')


def show_scatters(data_list):
    for k, v in data_list.items():
        show_scatter(k, v)


def show_scatter(ticker, data):
    print(f'Calculating scatters for {ticker}')
    scatter_matrix(data)
    pyplot.savefig(f'data/scatter_{ticker}.png')


def create_chart(data_list):
    pyplot.figure()
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
    stock_list = get_stock_list(data_list)

    print('Saving data')
    with open(f"data/stock_data.json", "w") as file:
        file.write(json.dumps(stock_list, indent=4))


def get_stock_list(data_list):
    stock_list = {}
    for k, v in data_list.items():
        data_json = v.to_json()
        stock_list[k] = json.loads(data_json)
    return stock_list


if __name__ == "__main__":
    main()

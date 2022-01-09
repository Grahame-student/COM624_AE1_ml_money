import datetime as dt

import numpy
import pandas
import pandas_datareader.data as pdr

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class FinancialModel:
    def __init__(self, ticker="", start_date=dt.datetime(1970, 1, 1), end_date=dt.datetime.now()):
        self.data = None            # Exposed data
        self.__initial_data = None  # Copy of downloaded data that we can roll back to
        # days to look ahead by
        self.look_ahead = 20
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def get_data(self):
        print(f'Requesting financial data for: {self.ticker}')
        try:
            data = pdr.get_data_yahoo(self.ticker, self.start_date, self.end_date)
            data['date_time'] = pandas.to_datetime(data.index)
            data['date_time_unix'] = pandas.to_numeric(data.date_time)
            data.index = data['date_time']
            self.__initial_data = data.drop(['date_time'], axis=1)
            self.__initial_data.reset_index(inplace=True)

        except Exception as e:
            print(str(e))
            print(f'Unable to fetch: {self.ticker}')

    def train(self):
        self.data = self.__initial_data.copy(deep=True)
        self.__get_profit()
        self.__clean_data()
        self.__linear_regression()

    def __get_profit(self):
        # Determine a pessimistic profit value for the selected prediction period
        if 'profit' in self.data:
            self.data = self.data[self.data.columns.drop('profit')]
        self.data[f'profit'] = self.data.Low - self.data.High.shift(self.look_ahead)
        self.data[f'range'] = self.data.High - self.data.Low

    def __clean_data(self):
        # Remove missing data
        columns = self.data.columns[:]
        print(self.data.isnull().sum().loc[columns])

        # Remove extreme outliers (> +/- 12 std_dev from mean) caused by highly suspect data
        self.data = self.data[(numpy.abs(self.data.profit - self.data.profit.mean()) < (12 * self.data.profit.std()))]

    def __linear_regression(self):
        train_headers = ['Open', 'High', 'Close', 'Volume', 'range', 'profit', 'date_time_unix']
        target_header = ['Low']

        x = self.data[train_headers]
        y = self.data[target_header]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, shuffle=False, random_state=0)

        regress = LinearRegression()
        regress.fit(x_train, y_train)

        prediction = numpy.append(y_train, regress.predict(x_test))
        self.data['pred'] = prediction.tolist()

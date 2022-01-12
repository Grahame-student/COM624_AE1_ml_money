import datetime
import datetime as dt

import numpy
import pandas
import pandas_datareader.data as pdr

from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from pykalman import KalmanFilter
from matplotlib import pyplot


class FinancialModel:
    def __init__(self, ticker="", start_date=dt.datetime(1970, 1, 1), end_date=dt.datetime.now()):
        self.data = None              # Exposed data
        self.__initial_data = None    # Copy of downloaded data that we can roll back to
        self.look_ahead = 20          # Number of days to look ahead by
        self.ticker = ticker          #
        self.start_date = start_date  #
        self.end_date = end_date      #

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

    def __add_date_features(self, data):
        data['year'] = pandas.DatetimeIndex(data['date_time']).year
        data['month'] = pandas.DatetimeIndex(data['date_time']).month
        data['day'] = pandas.DatetimeIndex(data['date_time']).day
        data['day_of_week'] = data['date_time'].dt.dayofweek

    def train(self):
        self.data = self.__initial_data.copy(deep=True)
        self.__get_profit()
        self.__clean_data()
        # self.__linear_regression()
        self.__polynomial_regression()
        # self.__time_series()

    def __get_profit(self):
        # Determine a pessimistic profit value for the selected prediction period
        if 'profit' in self.data:
            self.data = self.data[self.data.columns.drop('profit')]
        self.data[f'profit'] = self.data.Low - self.data.High.shift(self.look_ahead)
        self.data[f'range'] = self.data.High - self.data.Low

    def __clean_data(self):
        # Remove missing data
        columns = self.data.columns[:]
        # ID columns with null data
        print(self.data.isnull().sum().loc[columns])
        self.data.dropna(inplace=True)
        # ID columns with single value
        print(self.data.nunique())
        # ID rows with duplicate data
        print(self.data.duplicated().any())

        # Remove extreme outliers (> +/- 12 std_dev from mean) caused by highly suspect data
        self.data = self.data[(numpy.abs(self.data.profit - self.data.profit.mean()) < (12 * self.data.profit.std()))]

    def __linear_regression(self):
        filter_features = ['Low', 'Volume']
        train_header = ['date_time_unix']
        target_header = ['Low']

        # self.__kalman_filter_features(filter_features)

        train, test = self.__split_data()
        x_train = train[train_header]
        y_train = train[target_header]
        x_test = test[train_header]
        y_test = test[target_header]

        regress = LinearRegression()
        regress.fit(x_train, y_train)

        pred = regress.predict(x_test)
        print(f' MAE: {metrics.mean_absolute_error(y_test, pred)}')
        print(f' MSE: {metrics.mean_squared_error(y_test, pred)}')
        print(f'RMSE: {numpy.sqrt(metrics.mean_squared_error(y_test, pred))}')
        print(f'  R2: {metrics.r2_score(y_test, pred)}')

        prediction = numpy.append(y_train, pred)
        self.data['pred'] = prediction.tolist()

    def __split_data(self):
        # x = self.data[train_header]
        # y = self.data[target_header]
        # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, shuffle=False, random_state=0)
        train_end = datetime.datetime.now() - datetime.timedelta(days=self.look_ahead)
        train = self.data[self.data['date_time'] < train_end]
        test = self.data[self.data['date_time'] >= train_end]
        return train, test

    def __polynomial_regression(self):
        train_header = ['date_time_unix']
        target_header = ['Low']

        train, test = self.__split_data()
        x_train = train[train_header]
        y_train = train[target_header]
        x_test = test[train_header]
        y_test = test[target_header]

        poly_reg = PolynomialFeatures(degree=16)
        x_poly = poly_reg.fit_transform(x_train)
        regress = LinearRegression()
        regress.fit(x_poly, y_train)

        pred = regress.predict(poly_reg.fit_transform(x_test))
        print(f' MAE: {metrics.mean_absolute_error(y_test, pred)}')
        print(f' MSE: {metrics.mean_squared_error(y_test, pred)}')
        print(f'RMSE: {numpy.sqrt(metrics.mean_squared_error(y_test, pred))}')
        print(f'  R2: {metrics.r2_score(y_test, pred)}')

        prediction = numpy.append(y_train, pred)
        self.data['pred'] = prediction.tolist()

    def __kalman_filter_features(self, headers):
        kf = KalmanFilter(transition_matrices=[1],
                          observation_matrices=[1],
                          initial_state_mean=0,
                          initial_state_covariance=1,
                          observation_covariance=1,
                          transition_covariance=0.01)

        for feature in headers:
            self.__kalman_filter(kf, feature)

    def __kalman_filter(self, kf, feature):
        filtered, _ = kf.filter(self.data[feature])
        new_feature = f'kalman_{feature}'
        self.data[new_feature] = filtered

    # Useful methods for examining the data set
    def __corr_analysis(self, data):
        corr = data.corr()
        corr_fig = pyplot.figure()
        axis = corr_fig.add_subplot(111)
        axcorr = axis.matshow(corr, vmin=-1, vmax=1)
        corr_fig.colorbar(axcorr)
        ticks = numpy.arange(0, 12, 1)
        pyplot.xticks(rotation=90)
        axis.set_xticks(ticks)
        axis.set_yticks(ticks)
        axis.set_xticklabels(data.columns[:])
        axis.set_yticklabels(data.columns[:])

        pyplot.show()

    def __scatter_analysis(self, data):
        pandas.set_option('display.width', 1000)
        pandas.set_option('precision', 4)

        pandas.plotting.scatter_matrix(data)
        pyplot.show()

    def __data_stats(self, data):
        pandas.options.display.max_columns = data.shape[1]
        print(data.describe(include='all', datetime_is_numeric=True))
        print(data.head())

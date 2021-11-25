import datetime as dt
import pandas_datareader.data as pdr


class FinancialModel:
    def __init__(self, ticker="", start_date=dt.datetime(1970, 1, 1), end_date=dt.datetime.now()):
        self.data = None
        # days to look ahead by
        self.look_ahead = 20
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def get_data(self):
        print(f'Requesting financial data for: {self.ticker}')
        try:
            data = pdr.get_data_yahoo(self.ticker, self.start_date, self.end_date)
            self.data = data
            self.get_profit()
        except Exception as e:
            print(str(e))
            print(f'Unable to fetch: {self.ticker}')

    def get_profit(self):
        # Determine a pessimistic profit value for the selected prediction period
        if 'profit' in self.data:
            self.data = self.data[self.data.columns.drop('profit')]
        self.data[f'profit'] = self.data.Low - self.data.High.shift(self.look_ahead)

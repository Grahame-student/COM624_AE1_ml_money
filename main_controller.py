from datetime import timedelta

import companies


class MainController:
    def __init__(self, view, model):
        self.__view = view
        self.__model = model
        self.__connect_events()
        self.__populate_company_list()
        self.__set_default_company()
        self.__set_default_look_ahead()

    def __connect_events(self):
        self.__view.cbo_company.activated.connect(self.__on_company_changed)
        self.__view.txt_look_ahead.valueChanged.connect(self.__on_look_ahead_changed)

    def __populate_company_list(self):
        for company in companies.company_list:
            self.__view.add_company(company['name'], company["ticker"])

    def __set_default_company(self):
        index = self.__view.cbo_company.findText(companies.default_company)
        if index > -1:
            self.__view.cbo_company.setCurrentIndex(index)
            self.__on_company_changed(index)

    def __set_default_look_ahead(self):
        self.__view.txt_look_ahead.setValue(self.__model.look_ahead)

    def __plot_data(self):
        self.__view.chart_data.axes.cla()
        self.__view.chart_data.axes.set_title(self.__view.cbo_company.currentText())
        self.__view.chart_data.axes.plot(self.__model.data['date_time'], self.__model.data['Low'], linewidth=0.7,
                                         label='Low')
        self.__view.chart_data.axes.plot(self.__model.data['date_time'], self.__model.data['pred'], linewidth=0.7,
                                         label='Prediction')
        self.__view.chart_data.axes.set_xlim(
            [self.__model.end_date - timedelta(days=self.__model.look_ahead * 3), self.__model.end_date])
        self.__view.chart_data.axes.legend()
        self.__view.chart_data.draw()

    def __on_company_changed(self, index):
        self.__view.cbo_company.setEnabled(False)
        self.__get_ticker_data(self.__view.cbo_company.itemData(index))
        self.__view.cbo_company.setEnabled(True)

    def __get_ticker_data(self, ticker):
        self.__model.ticker = ticker
        self.__model.get_data()
        self.__model.train()
        self.__plot_data()

    def __on_look_ahead_changed(self):
        self.__model.look_ahead = self.__view.txt_look_ahead.value()
        self.__model.train()
        self.__plot_data()

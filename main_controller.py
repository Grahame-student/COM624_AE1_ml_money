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
        # Populate from a master list
        for company in companies.company_list:
            self.__view.add_company(company["name"], company["ticker"])

    def __set_default_company(self):
        index = self.__view.cbo_company.findText(companies.default_company)
        if index > -1:
            self.__view.cbo_company.setCurrentIndex(index)
            self.__on_company_changed(index)

    def __set_default_look_ahead(self):
        self.__view.txt_look_ahead.setValue(self.__model.look_ahead)

    def __get_ticker_data(self, ticker):
        self.__model.ticker = ticker
        self.__model.get_data()
        self.__plot_data()

    def __plot_data(self):
        self.__view.chart_data.axes.cla()
        financial_data = self.__model.data.copy(deep=True)
        financial_data = financial_data[financial_data.columns.drop('Volume')]
        financial_data.plot(ax=self.__view.chart_data.axes)
        self.__view.chart_data.draw()

    def __on_company_changed(self, index):
        self.__view.cbo_company.setEnabled(False)
        self.__get_ticker_data(self.__view.cbo_company.itemData(index))
        self.__view.cbo_company.setEnabled(True)

    def __on_look_ahead_changed(self):
        self.__model.look_ahead = self.__view.txt_look_ahead.value()
        self.__get_profit_data(self.__view.txt_look_ahead.value())

    def __get_profit_data(self, look_ahead):
        self.__model.look_ahead = look_ahead
        self.__model.get_profit()
        self.__plot_data()

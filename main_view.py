from PyQt5 import QtCore, QtWidgets

from FinancialCanvas import FinancialCanvas


class UiMainWindow(object):
    def __init__(self):
        self.chart_data = None

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(798, 544)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.chart_data = FinancialCanvas(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.chart_data.sizePolicy().hasHeightForWidth())
        self.chart_data.setSizePolicy(sizePolicy)
        self.chart_data.setObjectName("chart_data")
        self.gridLayout.addWidget(self.chart_data, 0, 0, 1, 2)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.lbl_company = QtWidgets.QLabel(self.centralwidget)
        self.lbl_company.setObjectName("lbl_company")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_company)
        self.cbo_company = QtWidgets.QComboBox(self.centralwidget)
        self.cbo_company.setObjectName("cbo_company")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbo_company)
        self.lbl_look_ahead = QtWidgets.QLabel(self.centralwidget)
        self.lbl_look_ahead.setObjectName("lbl_look_ahead")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_look_ahead)
        self.txt_look_ahead = QtWidgets.QSpinBox(self.centralwidget)
        self.txt_look_ahead.setObjectName("txt_look_ahead")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_look_ahead)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_company.setText(_translate("MainWindow", "Company"))
        self.lbl_look_ahead.setText(_translate("MainWindow", "Prediction Period (days)"))

    def add_company(self, company, ticker_id):
        self.cbo_company.addItem(company, ticker_id)
        self.cbo_company.model().sort(0)

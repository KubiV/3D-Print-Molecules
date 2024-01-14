# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(877, 687)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(60, 130, 591, 121))
        self.tableView.setObjectName("tableView")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(70, 350, 591, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.preview = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.preview.setContentsMargins(0, 0, 0, 0)
        self.preview.setObjectName("preview")
        self.qualitySlider = QtWidgets.QSlider(self.centralwidget)
        self.qualitySlider.setGeometry(QtCore.QRect(180, 270, 160, 22))
        self.qualitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.qualitySlider.setObjectName("qualitySlider")
        self.quality = QtWidgets.QTextBrowser(self.centralwidget)
        self.quality.setGeometry(QtCore.QRect(60, 260, 111, 41))
        self.quality.setObjectName("quality")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 10, 581, 111))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.browseFiles = QtWidgets.QPushButton(self.widget)
        self.browseFiles.setObjectName("browseFiles")
        self.gridLayout_2.addWidget(self.browseFiles, 1, 0, 1, 1)
        self.getData = QtWidgets.QPushButton(self.widget)
        self.getData.setObjectName("getData")
        self.gridLayout_2.addWidget(self.getData, 0, 2, 1, 1)
        self.fileName = QtWidgets.QTextBrowser(self.widget)
        self.fileName.setObjectName("fileName")
        self.gridLayout_2.addWidget(self.fileName, 1, 1, 1, 2)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 2)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(400, 270, 261, 41))
        self.widget1.setObjectName("widget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.selectExportPath = QtWidgets.QPushButton(self.widget1)
        self.selectExportPath.setObjectName("selectExportPath")
        self.gridLayout_3.addWidget(self.selectExportPath, 0, 0, 1, 1)
        self.exportPath_2 = QtWidgets.QTextBrowser(self.widget1)
        self.exportPath_2.setObjectName("exportPath_2")
        self.gridLayout_3.addWidget(self.exportPath_2, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 877, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.getData.clicked.connect(self.textEdit.copy) # type: ignore
        self.browseFiles.clicked.connect(self.fileName.reload) # type: ignore
        self.qualitySlider.valueChanged['int'].connect(self.quality.reload) # type: ignore
        self.selectExportPath.clicked.connect(self.exportPath_2.reload) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.quality.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Kvalita:</p></body></html>"))
        self.browseFiles.setText(_translate("MainWindow", "Procházet soubory"))
        self.getData.setText(_translate("MainWindow", "Získat data"))
        self.selectExportPath.setText(_translate("MainWindow", "Složka pro export"))
        self.exportPath_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">/...</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

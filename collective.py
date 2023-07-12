from collective_ui import Ui_Collective
from color_scheduler import Scheduler
from report_filter import Scraper
import sys, os, os.path
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidgetItem, QMainWindow
)
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtWidgets
import atexit


class Collective(QWidget):
    
    def __init__(self):
        super().__init__()

        self.ui = Ui_Collective()
        self.uis = QtWidgets.QMainWindow()

        self.ui.setupUi(self.uis)

        self.cs = Scheduler(self.ui)
        self.rf = Scraper(self.ui)

        self.uis.show()


        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    collective_window = Collective()
    sys.exit(app.exec())


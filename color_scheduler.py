import sys, os, csv, os.path
from collective_ui import Ui_Collective
from color_helper import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QHeaderView
)

class Scheduler(QWidget, Ui_Collective):
    file_seq = ""
    file_truck = ""

    seq_contents = None
    truck_contents = None

    seq_dict = {}
    inc_dict = {}

    seq_cells = None
    truck_cells = None

    color_col = None
    qty_col = None

    defRowCount = None

    write_list = []

    def __init__(self, collective):
        super().__init__()

        # collective = Ui_Collective()
        # collective.setupUi(self)

        # Make UI changes
        ui_changes(self, collective)


        # Define vars/components
        btnImpTC = collective.btnImpTC
        btnImpCS = collective.btnImpCS
        btnResetCS = collective.btnResetCS
        btnVis = collective.btnVisualize
        btnSaveCS = collective.btnSaveCS
        self.defRowCount = collective.tblOutputCS.rowCount()


        # # Connect events
        btnImpTC.clicked.connect(lambda: self.truck_handler(collective))
        btnImpCS.clicked.connect(lambda: self.seq_handler(collective))
        btnResetCS.clicked.connect(lambda: self.reset_handler(collective))
        btnVis.clicked.connect(lambda: self.vis_handler(collective))
        btnSaveCS.clicked.connect(lambda: self.save_handler(collective))

        # with open('styles.qss', 'r') as f:
        #     style = f.read()
        #     self.setStyleSheet(style)

    def truck_handler(self, collective):

        lblTruck = collective.lblTruck

        filename = callback()

        if (filename == ''):
            return
        elif (filename == "ERR"):
            lblTruck.setText("Error, wrong file format.")
            return
        
        # Abbreviate the file path
        modf = os.path.basename(filename)

        # Set the label to the file path
        lblTruck.setText(modf)

        # Open the file
        self.file_truck = file_open(self, filename)

        # Read in the file
        self.truck_contents = file_read(self, self.file_truck)

        # Parse the data
        self.truck_cells = str(self.truck_contents[1]).split(',')

        # Get the columns of the desired properties
        for idx, ele in enumerate(self.truck_cells):
            if (ele == "Color"):
                self.color_col = idx
            elif (ele == "QT"):
                self.qty_col = idx
            


    def seq_handler(self, collective):

        lblColorSeq = collective.lblColorSeq
        
        filename = callback()

        if (filename == ''):
            return
        elif (filename == "ERR"):
            lblColorSeq.setText("Error, wrong file format.")
            return
        
        # Abbreviate the file path
        modf = os.path.basename(filename)

        # Set the label to the file path
        lblColorSeq.setText(modf)

        # Open the file
        self.file_seq = file_open(self, filename)

        # Read in the file
        self.seq_contents = file_read(self, self.file_seq)

        # Create a dictionary that contains color and quantity
        for color in self.seq_contents:
            color = color.replace('\n', '')
            color = color.replace(' ', '')
            self.seq_dict[color] = 0
        
    def vis_handler(self, collective):
        wFormat = 0
        accuracy = 0
        totalEntries = 0
        totalQuantity = 0
        self.write_list = []

        # Zero the dictionaries
        self.seq_dict = { color: 0 for color in self.seq_dict }
        self.inc_dict = {}

        # Clear previous table content
        collective.tblOutputCS.clearContents()
        collective.tblOutputCS.setRowCount(self.defRowCount)

        # Null check necessary parameters
        if (self.seq_dict == {} or self.truck_contents == None):
            return
        
        # Loop through the given entries
        for idx, row in enumerate(self.truck_contents):
            e_color = None

            # Separate the row by cells
            self.truck_cells = str(row).split(',')

            # Isolate the color variable
            p_color = e_color = self.truck_cells[self.color_col]

            # Skip header fields
            if (e_color == '' or e_color == "Color"):
                continue

            # Isolate the qty variable
            qty = int(self.truck_cells[self.qty_col])


            # If color exists in dictionary, add its qty to the dict
            e_color = e_color.replace('\n', '')
            e_color = e_color.replace(' ', '')

            # Determine if entry color is within the dict and increment the counter
            if e_color in self.seq_dict:
                self.seq_dict[e_color] += qty
            else:
                # Add incompatible color to inc_dict
                if p_color in self.inc_dict:
                    self.inc_dict[p_color] += qty
                else:
                    self.inc_dict[p_color] = qty
                # Increment incompatible counter
                wFormat += 1
            
            totalQuantity += qty
            totalEntries += 1

        # Determine the accuracy and total entries of the sort
        accuracy = (1 - (wFormat / totalEntries)) * 100

        lblAcc = collective.lblAccuracy
        lblAcc.setText(str("{:.2f}".format(accuracy)) + '%')

        lblTotal = collective.lblTotal
        lblTotal.setText(str(totalEntries))

        lblQuantity = collective.lblQuantity
        lblQuantity.setText(str(totalQuantity))

        # Determine the number of rows needed
        maxRowCount = 0
        for color in self.seq_dict:
            if self.seq_dict[color] > 0:
                maxRowCount += 1
        
        # Set the table row count
        maxRowCount += len(self.inc_dict)
        collective.tblOutputCS.setRowCount(maxRowCount)

        # Populate the table with valid sorts
        rowCounter = 0
        for rowidx, color in enumerate(self.seq_contents):
            modc = color.replace('\n', '')
            modc = modc.replace(' ', '')


            if (self.seq_dict[modc] > 0):
                collective.tblOutputCS.setItem(rowCounter, 0, QTableWidgetItem(color))
                collective.tblOutputCS.setItem(rowCounter, 1, QTableWidgetItem(str(self.seq_dict[modc])))
                self.write_list.append(color.replace('\n', '') + ',' + str(self.seq_dict[modc]) + '\n')
                rowCounter += 1


        if accuracy < 100:
            collective.tblOutputCS.setRowCount(maxRowCount + 2)

            # Skip a row for white space
            rowCounter += 1

            # Insert Lower Header
            collective.tblOutputCS.setSpan(rowCounter, 0, 1, 2)
            collective.tblOutputCS.setItem(rowCounter, 0, QTableWidgetItem("Unmatched Colors"))
            self.write_list.append('\n')
            self.write_list.append("Unmatched Colors:\n")
            rowCounter += 1

            # Add in all incompatible colors
            for color in self.inc_dict:
                collective.tblOutputCS.setItem(rowCounter, 0, QTableWidgetItem(color))
                collective.tblOutputCS.setItem(rowCounter, 1, QTableWidgetItem(str(self.inc_dict[color])))
                self.write_list.append(color.replace('\n', '') + ',' + str(self.inc_dict[color]) + '\n')
                rowCounter += 1

    def save_handler(self, collective):
        savedFilename = asksaveasfilename()

        # Null check
        if (savedFilename == '' or self.write_list == []):
            return

        newFile = open(savedFilename, 'w')

        newFile.writelines(self.write_list)

        newFile.close()




    def reset_handler(self, collective):
        collective.lblTruck.setText("Imported file ...")
        collective.lblColorSeq.setText("Imported file ...")

        lblAcc = collective.lblAccuracy
        lblAcc.setText('')

        lblTotal = collective.lblTotal
        lblTotal.setText('')

        lblQuantity = collective.lblQuantity
        lblQuantity.setText('')

        collective.tblOutputCS.clearContents()
        collective.tblOutputCS.setRowCount(self.defRowCount)

        self.file_seq = ""
        self.file_truck = ""

        self.seq_contents = None
        self.truck_contents = None

        self.seq_dict = {}
        self.inc_dict = {}

        self.seq_cells = None
        self.truck_cells = None

        self.color_col = None
        self.write_list = []


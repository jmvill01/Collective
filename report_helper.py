import os, os.path
from tkinter import *
from tkinter.filedialog import askopenfilename
from PyQt6.QtWidgets import (
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import *
from PyQt6.QtCore import *


def callback():
    # Prompt the user for a file
    filename = askopenfilename()

    # Gather just the extension from the filename
    ext = os.path.splitext(filename)[1]

    # Verify the user input a valid file
    if (ext != ".csv"):
        filename = 'ERR'

    return filename

def ui_changes(self, collective):

    # Perform all ui changes outside of the designer
    collective.lblFile.setStyleSheet("color: gray;")
    collective.lblErr.setStyleSheet("color: gray;")

    collective.inpDate.setPlaceholderText("00/00/00")
    collective.inpType.setPlaceholderText("Base, Wall, etc.")
    collective.tblOutputRF.setColumnCount(5)
    collective.tblOutputRF.setRowCount(5)
    collective.tblOutputRF.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)      
    collective.tblOutputRF.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    collective.inpCreateMacro.setPlaceholderText("Macro name ...")
    collective.inpCreateMod.setPlaceholderText("Mod name ...")

    collective.comMacros.addItem("None Selected")
    collective.comDeleteMod.addItem("None Selected")
    collective.comDeleteMacro.addItem("None Selected")


def file_open(self, filename):
    self.file = open(filename, 'r')

def file_read(self, handler):
    return handler.readlines()

def print_table(self, content, collective):
    tblOutputRF = collective.tblOutputRF
    tblOutputRF.clear()

    # Reset err label
    lblErr = collective.lblErr
    lblErr.setText("")

    maxCols = 0


    # Start looping through all table cells (row and column indexes)
    for rowidx, row in enumerate(content):
        rowItems = row.split(',')
        for colidx, item in enumerate(rowItems):
            collective.tblOutputRF.setRowCount(len(content))
            if (len(rowItems) > maxCols):
                maxCols = len(rowItems)
                collective.tblOutputRF.setColumnCount(maxCols)
            collective.tblOutputRF.setItem(rowidx, colidx, QTableWidgetItem(item))

    # Null check, set err label if needed
    if (collective.tblOutputRF.item(0,0) == None):
        lblErr.setText("No entries recorded.")
        return

    # Set table to resize to its contents
    # collective.tblOutputRF.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)      
    # collective.tblOutputRF.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

def strip_content(self, content):
    result = []
    row = []
    content = content.split(',')

    # Find all relevant columns, append to printable row
    row.append(content[self.truck_col])
    row.append(content[self.order_col])
    row.append(content[self.line_col])
    row.append(content[self.item_col])

    # Append all additional modifiers to the end of the row
    if (len(content) > self.mod_col):
        for idx in range(self.mod_col, len(content)):
            row.append(content[idx])
    else:
        row.append(content[self.mod_col])

    # Convert the list to a string and return
    finishedRow = list_string(row)
    result.append(finishedRow)
    return result

def read_macro_table(self, collective):

    # Create TEMPORARY test data
    # self.macro_handler = open(self.MACRO_PATH, 'w')

    # self.macro_handler.write("MACROS, MODS\n Setup, DJGIE, EKDJ, EKJ\n Assem, DBEE, DBKT")

    # self.macro_handler.close()

    # Read in the macro table    
    self.macro_handler = open(self.MACRO_PATH, 'r')

    # Error handle 
    if not self.macro_handler:
        print("File read did not occur.")
        return

    # Grab header
    self.macro_headers = self.macro_handler.readline()
    
    # Grab the rest of the content
    self.macro_contents = self.macro_handler.readlines()


    # Isolate the rows 
    for entry in self.macro_contents:
        row = entry.split(',')
        for idx, ele in enumerate(row):
            ele = ele.replace(' ', '')
            ele = ele.replace('\n', '')
            row[idx] = ele

        self.macro_mods.append(row)

    # Populates the list with all macros
    for row in self.macro_mods:
        self.macros.append(row[0])
            

    self.macro_handler.close()

    # Open the file, now in write mode
    self.macro_handler = open(self.MACRO_PATH, 'w')

    # Error handle
    if not self.macro_handler:
        print("File to write in did not open.")

    # Populate combo boxes with initial options
    populate_macro_combo_boxes(self, collective)

def populate_macro_combo_boxes(self, collective):            
    comMacros = collective.comMacros
    comDeleteMacro = collective.comDeleteMacro
    comMacros.clear()
    comDeleteMacro.clear()

    comMacros.addItem("None Selected")
    comDeleteMacro.addItem("None Selected")

    for macro in self.macros:
        comMacros.addItem(macro)
        comDeleteMacro.addItem(macro)

def populate_mod_combo_boxes(self, collective):
    comDeleteMod = collective.comDeleteMod
    comDeleteMod.clear()

    comDeleteMod.addItem("None Selected")

    if self.current_macro == "None Selected":
        for mod in self.none_mods:
            comDeleteMod.addItem(mod)
        return

    for mod in self.current_mods:
        comDeleteMod.addItem(mod)

def format_string(self, row_contents, mods):

    row = row_contents.split(',')
    newRow = ''

    for idx, item in enumerate(row):
        if idx >= 4:
            break
        newRow += item + ','

    for idx, mod in enumerate(mods):
        if idx >= len(mods):
            newRow += mod
        else:
            newRow += mod + ','

    return newRow

def write_sequence(self):
    # This function is run as an auto-save feature, but also on program
    # exit. Therefore preventing significant data loss

    debug(self)

    # Opens file if file has previously been closed
    if self.macro_handler.closed:
        self.macro_handler = open(self.MACRO_PATH, 'w')

    # Writes in headers
    self.macro_handler.write("MACROS, MODS\n")

    # Writes in all macros
    for macro in self.macro_mods:
        newMacro = list_string(macro)
        self.macro_handler.write(newMacro + '\n')

    # Closes the file
    self.macro_handler.close()

    
# Converts a list to a string, delimited by commas
def list_string(list):
    conversion = ""

    conversion = ', '.join([str(ele) for ele in list])

    return conversion

def debug(self):
    print("\n-------------------- Variable Evaluation: --------------------")
    print('\ncurrent_macro:', self.current_macro, '\n')
    print('\ncurrent_mods:', self.current_mods, '\n')

    print('\nmacro_mods: ', self.macro_mods, '\n')
    print('\nmacros: ', self.macros, '\n')
    print('\nmacro_contents: ', self.macro_contents, '\n')
    print("\n-------------------- End Evaluation --------------------\n")




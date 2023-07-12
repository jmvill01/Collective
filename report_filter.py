import sys, os, os.path
from dateutil.parser import parse
from datetime import datetime
from collective_ui import Ui_Collective
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTableWidgetItem
)
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from report_helper import *
import atexit


class Scraper(QWidget, Ui_Collective):
    file = None
    file_contents = None
    filtered_contents = []
    filtered_line = []
    curr_line = []

    type_param = None
    date_param = None

    type_col = None
    date_col = None
    truck_col = None
    order_col = None
    line_col = None
    item_col = None
    mod_col = None

    # Reflect all path changes to resource file here
    DIR_NAME = os.path.dirname(__file__)
    MACRO_PATH = os.path.dirname(DIR_NAME) + '\_res\macro_mods.csv'

    # Auto save rate (ms)
    AUTO_SAVE = 15000

    # Macro variables
    macro_handler = None
    macro_headers = None
    macro_contents = []
    macros = []
    macro_mods = []
    current_macro = None
    current_mods = []
    none_mods = []

    def __init__(self, collective):
        super().__init__()

        # Make UI changes
        ui_changes(self, collective)

        # Read in Macro table
        read_macro_table(self, collective)


        # Define vars/components
        btnimp = collective.btnImport
        btnFilter = collective.btnFilter
        btnResetRF = collective.btnResetRF
        btnSaveRF = collective.btnSaveRF
        btnCreateMacro = collective.btnCreateMacro
        btnDeleteMacro = collective.btnDeleteMacro
        btnDeleteMod = collective.btnDeleteMod
        btnApplyMod = collective.btnApplyMod
        comMacros = collective.comMacros
        btnFilterMacro = collective.btnFilterMacro

        self.current_macro = collective.comMacros.currentText()

        # Connect events
        btnimp.clicked.connect(lambda: self.file_handler(collective))
        btnFilter.clicked.connect(lambda: self.content_handler(collective))
        btnResetRF.clicked.connect(lambda: self.reset_handler(collective))
        btnSaveRF.clicked.connect(lambda: self.save_handler(collective))
        btnCreateMacro.clicked.connect(lambda: self.create_macro(collective))
        btnDeleteMacro.clicked.connect(lambda: self.delete_macro(collective))
        btnDeleteMod.clicked.connect(lambda: self.delete_mod(collective))
        btnApplyMod.clicked.connect(lambda: self.create_mod(collective))
        comMacros.currentTextChanged.connect(lambda: self.change_macro(collective))
        btnFilterMacro.clicked.connect(lambda: self.filter_table(collective))

        # Start auto-save sequence (15 seconds)
        timer_handler = self.startTimer(self.AUTO_SAVE)
        
        atexit.register(self.exit_sequence)
 

    # ---------------------- Referenced from Stack Overflow ---------------------- 
    # This code allows the table to have copy and paste functionality
    def keyPressEvent(self, event, collective):
        super().keyPressEvent(event, collective)
       
        if event.key() == Qt.Key.Key_C and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.copied_cells = sorted(collective.tblOutputRF.selectedIndexes())
        elif event.key() == Qt.Key.Key_V and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            r = collective.tblOutputRF.currentRow() - self.copied_cells[0].row()
            c = collective.tblOutputRF.currentColumn() - self.copied_cells[0].column()
            for cell in self.copied_cells:
                collective.tblOutputRF.setItem(cell.row() + r, cell.column() + c, QTableWidgetItem(cell.data()))

    # --------- https://stackoverflow.com/questions/60715462/how-to-copy-and-paste-multiple-cells-in-qtablewidget-in-pyqt5 ---------

    # ------------- Auto-saving functionality -------------
    # Prevents:
    #   - Significant loss of data
    #       - Macros
    #       - Mods
    # Addresses Impact of:
    #   - Computer Shutdowns
    #   - Program crash events
    #   - Other data loss events
    # ------------------------------------------------------
    def timerEvent(self, event):
        write_sequence(self)

    def file_handler(self, collective):

        # Get user's file
        filename = callback()

        lblImpFile = collective.lblFile

        # Error handle
        if (filename == ''):
            return
        elif (filename == "ERR"):
            lblImpFile.setText("Error, wrong file format.")
            return

        # Abbreviate the file path
        modf = os.path.basename(filename)

        # Set the label to the file path
        lblImpFile.setText(modf)


        # Open the file | Fills the handler
        file_open(self, filename)

        # Read the file
        self.file_contents = file_read(self, self.file)
        
        # Close the file
        self.file.close()

    def content_handler(self, collective):

        # Empty output text
        self.filtered_contents.clear()
        self.filtered_line.clear()
        self.curr_line.clear()
        
        # Get parameters
        type = collective.inpType.text()
        date = collective.inpDate.text()

        # Fill the parameters from the inputs
        self.type_param = type
        self.date_param = date

        # Null check
        if (self.file_contents == None or self.file_contents == []):
            return

        # Fill the curr_line var with data
        self.curr_line = str(self.file_contents[1]).split(',')

        # Get the columns of the filtration attributes
        for idx, ele in enumerate(self.curr_line):
            if (ele == "Attribute"):
                self.type_col = idx
            elif(ele == "Sched Date"):
                self.date_col = idx
            elif(ele == "Truck"):
                self.truck_col = idx
            elif(ele == "Order"):
                self.order_col = idx
            elif (ele == "Line"):
                self.line_col = idx
            elif(ele == "Item"):
                self.item_col = idx
            elif(ele == "MODS\n" or ele == "MODS"):
                self.mod_col = idx
                print(idx)

        correctFormat = "%m/%d/%y"
        form1 = "%m/%d/%Y"
        form2 = "%m/%d/%y"
        form = None

        # Evaluate all rows to determine
        for idx, row in enumerate(self.file_contents):

            tFlag = dFlag = False
            self.curr_line = row.split(',')

            print(self.curr_line)
            # Handle starting row
            if (idx < 2):
                print(idx, '\n')
                continue



            rowDate = str(self.curr_line[self.date_col])


            # Check row dates for particular formats
            try:
                success = bool(datetime.strptime(rowDate, form1))
                date = datetime.strptime(rowDate, form1)
            except ValueError:
                success = False
            
            if not success:
                try:
                    success = bool(datetime.strptime(date, form2))
                    date = datetime.strptime(date, form2)
                except ValueError:
                    success = False
            
            # If no correct format was found, go on to next iteration
            if not success:
                print("Date incorrectly formatted: ", idx)
                continue


        

            date = datetime.strftime(date, correctFormat)

            if (date == str(self.date_param)):
                dFlag = True

            if (str(self.curr_line[self.type_col]) == str(self.type_param)):
                tFlag = True

            if (tFlag and dFlag):

                # Strip the row of unnecessary data
                cleanedContent = strip_content(self, row)

                # Turn it into a string
                cleanedRow = list_string(cleanedContent)

                # Append the row to the filtered_contents array
                self.filtered_contents.append(cleanedRow)

        print_table(self, self.filtered_contents, collective)
        
    def reset_handler(self, collective):

        # Empty output text
        self.filtered_contents.clear()
        self.filtered_line.clear()
        self.curr_line.clear()
        collective.tblOutputRF.clearContents()

        collective.inpType.clear()
        collective.inpDate.clear()

        ui_changes(self, collective)

        lblImpFile = collective.lblFile
        lblImpFile.setText("Imported file ...")

        # Reset err label
        lblErr = collective.lblErr
        lblErr.setText("")

        # Reset current variables
        self.current_macro = None
        self.current_mods = []
        self.none_mods = []

        # Reset inputs
        populate_macro_combo_boxes(self, collective)
        populate_mod_combo_boxes(self, collective)

        inpCreateMacro = collective.inpCreateMacro
        inpCreateMacro.clear()

        inpCreateMod = collective.inpCreateMod
        inpCreateMod.clear()

        checkFollowNum = collective.checkFollowNum
        checkFollowNum.setChecked(False)


    def save_handler(self, collective):
        printData = []

        savedFilename = asksaveasfilename()

        # Error handling
        if (savedFilename == ''):
            return

        fields = ['Truck,', 'Order,', 'Line,', 'Item,', 'MODS,']

        newFile = open(savedFilename, 'w')

        # Get the axis counts for valid loops 
        colCount = collective.tblOutputRF.columnCount()
        rowCount = collective.tblOutputRF.rowCount()

        # Collects all the data from the table
        for row in range(0, rowCount):
            for column in range(0, colCount):
                if (collective.tblOutputRF.item(row, column) != None):
                    cell = collective.tblOutputRF.item(row, column).text()
                    cell += ','
                    printData.append(cell)

            printData.append('\n')

        
        # Writes each element to the file
        for ele in printData:
            newFile.write(str(ele))

        # Close the file
        newFile.close()

    def create_macro(self, collective):

        # Get the Macro Name
        inpCreateMacro = collective.inpCreateMacro
        newMacro = inpCreateMacro.text()
        
        # Error handle
        if not self.macro_handler or newMacro == '':
            return
        
        self.macros.append(newMacro)
        self.macro_mods.append([newMacro])
        
        # Reset input field
        inpCreateMacro.setText('')

        populate_macro_combo_boxes(self, collective)

        comMacros = collective.comMacros
        comMacros.setCurrentText(newMacro)


    def delete_macro(self, collective):
        # Get the macro to delete
        comDeleteMacro = collective.comDeleteMacro
        delMacro = comDeleteMacro.currentText()

        # Remove the correct macro from macros
        for idx, macro in enumerate(self.macros):
            if macro == delMacro:
                del self.macros[idx]

        # Remove the correct macro from macro_mods
        for idx, macro in enumerate(self.macro_mods):
            if macro[0] == delMacro:
                del self.macro_mods[idx]

        # Repopulate combo boxes with revised option list
        populate_macro_combo_boxes(self, collective)

        debug(self)

    def change_macro(self, collective):

        self.current_mods = []
        listMods = collective.listMods
        listMods.clear()

        # Set the latest macro
        comMacros = collective.comMacros
        self.current_macro = comMacros.currentText()

        # Error handle
        if self.current_macro == "None Selected":
            self.current_mods = self.none_mods
            populate_mod_combo_boxes(self, collective)

            # Populate the list on the side with the mods
            for mod in self.none_mods:
                listMods.addItem(mod)
            return 
              
        # Add the macros corresponding mods
        for idx, macro in enumerate(self.macro_mods):
            if (macro[0] == self.current_macro):
                for mod in macro[1:]:
                    self.current_mods.append(mod)

        # Populate the list on the side with the mods
        for mod in self.current_mods:
            listMods.addItem(mod)

        # Repopulate the mod combo boxes
        populate_mod_combo_boxes(self, collective)


    def create_mod(self, collective):
        inpCreateMod = collective.inpCreateMod
        newMod = inpCreateMod.text()
        newMod = newMod.upper()
        checkFollowNum = collective.checkFollowNum
        fNumFlag = checkFollowNum.isChecked()
        inpCreateMod.clear()
        checkFollowNum.setChecked(False)

        if newMod == '':
            return

        # Handle precursor mods
        if fNumFlag:
            newMod += '#'


        # Handle duplicate mods
        for mod in self.current_mods:
            if newMod == mod:
                return

        # Temporary filter when macro is None Selected
        if self.current_macro == "None Selected":
            listMods = collective.listMods
            listMods.clear()

            self.current_mods.append(newMod)
            self.none_mods = self.current_mods

            # Repopulate the mod combo boxes
            for mod in self.current_mods:
                listMods.addItem(mod)

            populate_mod_combo_boxes(self, collective)
        else:
            self.current_mods.append(newMod)

            newMacro = [self.current_macro]

            for ele in self.current_mods:
                newMacro.append(ele)

            # Reflect addition within macro_mods
            for idx, ele in enumerate(self.macro_mods):
                if ele[0] == self.current_macro:
                    self.macro_mods[idx] = newMacro

            # Repopulate the mod combo boxes
            self.change_macro(collective)
            # populate_mod_combo_boxes(self, collective)



    def delete_mod(self, collective):
        comDeleteMod = collective.comDeleteMod
        delMod = comDeleteMod.currentText()

        if delMod == "None Selected":
            return

        # Begin crafting new macro
        newMacro = [self.current_macro]

        # Account for None Selected macro
        if self.current_macro == "None Selected":
            self.current_mods = self.none_mods

        # Find the index of the mod to be deleted and formulate newest macro
        delIdx = None
        for idx, ele in enumerate(self.current_mods):
            if ele == delMod:
                delIdx = idx
            else:
                newMacro.append(self.current_mods[idx])

        # Use the index to delete the mod
        del self.current_mods[delIdx]

        if self.current_macro == "None Selected":
            self.none_mods = self.current_mods

        # Reflect deletion within macro_mods
        for idx, ele in enumerate(self.macro_mods):
            if ele[0] == self.current_macro:
                self.macro_mods[idx] = newMacro

        debug(self)

        # populate_mod_combo_boxes(self, collective)
        self.change_macro(collective)
        debug(self)

    def filter_table(self, collective):

        # Corresponds with the location of "Mods" header in the table
        mod_col = 4

        if self.filtered_contents == []:
            print("No contents to filter")
            return

        # Secure the entirety of the available content. This is temporary data        
        table_data = self.filtered_contents
        printed_data = []

        # Iterate row by row through each of the entries
        for rowidx, row in enumerate(table_data):
            mod_list = []
            rowItems = row.split(',')

            # Check for the Mods column
            for idx in range(mod_col, len(rowItems)):
                cmod = rowItems[idx]
                cmod = cmod.replace(' ', '')
                cmod = cmod.replace('\n', '')
                cmod = cmod.upper()

                # Iterate through every mod and compare against self.current_mods
                for mod in self.current_mods:
                    precursorFlag = False
                    mod = mod.upper()

                    # Check for precursor mods (mods with measurements that follow)
                    if '#' in mod:
                        precursorFlag = True
                        mod = mod.replace('#', '')
                        pre_cmod = ''.join([char for char in cmod if not char.isdigit()])
                        pre_cmod = pre_cmod.replace('.', '')

                        # If digitless mod matches the precursor mod then we append 
                        # original cmod to mod_list
                        if pre_cmod == mod:
                            mod_list.append(cmod)
                        continue
                    if cmod == mod:

                        mod_list.append(mod)
                
            mod_row = format_string(self, row, mod_list)

            # Append row to the new list
            printed_data.append(mod_row)

        # print the table
        print_table(self, printed_data, collective)

    def exit_sequence(self):
        # Engage write sequence
        write_sequence(self)

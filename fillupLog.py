from tkinter import *
from tkinter.ttk import *
import csv
import os
import sys

##############TODO###############################TODO#################
# REFACTOR as much as I can
# Research making my app a 'finished project'
# add some color/styling
#     * alternate bg color of rows
#     * play with padding/sticky etc to get a cleaner look
# Add input validation
# Add a help dialog (options):
#   * maybe create a popup window with a quick help message
#   * create a seperate page to 'tkraise'
#
##############TODO###############################TODO##################

class App(Tk):
    '''
    Main app class

    Main class which handles the appearnace of all GUI components and windows
    '''

    def __init__(self):
        '''
        initialize Tk
        '''
        Tk.__init__(self)

        self.menuBar()
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # not needed until multiple pages

        frame = GasLog(container, self)
        self.frames[GasLog] = frame
        frame.grid(sticky='nsew')

        self.show_frame(GasLog)

    def menuBar(self):
        menubar = Menu(self)
        self.config(menu=menubar)
        filemenu = Menu(menubar)
        menubar.add_cascade(label='File', menu=filemenu)

        def doPrint():
            print('doPrint')
        def doSave(): print('doSave')
        filemenu.add_command(label="Print", command=doPrint)
        filemenu.add_command(label='Save', command=doSave)
        filemenu.add_command(label="Exit", command=self.quit)


    def show_frame(self, cont):
        '''
        switch between visible windows

        takes one positional argument, which is the 'window' or 'page' that
        is to be 'brought foreward'
        '''
        frame = self.frames[cont]
        frame.tkraise()


class GasLog(Frame):
    '''
    Main GUI window

    contains functions to create table and entry fields for manipulating Gas
    log data. contains both visual and back-end functions
    '''

    def __init__(self, parent, controller):
        '''
        initialize gasLog frame as well as call functions to load all child
        components
        '''
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.path = sys.path[0]

        # initialize all componets of GUI
        self.createLog()
        self.loadData()
        self.createEntry()

    def createLog(self):
        '''
        create Treeview 'table' to view log entries
        '''

        self.tbl = Treeview(self)
        self.treeScroll = Scrollbar(self, orient='vertical',
                                    command=self.tbl.yview)
        self.treeScroll.configure(command=self.tbl.yview)
        self.tbl.configure(yscrollcommand=self.treeScroll.set)
        self.tbl['columns'] = ('date', 'odometer', 'tripometer', 'gallons',
                               'ppg', 'total')
        self.tbl.heading("#0", text="No.")
        self.tbl.column("#0", width=75, anchor='center')
        for n in self.tbl['columns']:
            self.tbl.heading(n, text=n)
            self.tbl.column(n, width=100, anchor='center')
        self.tbl.bind('<ButtonRelease-1>', self.selectItem)
        # self.tbl.bind('<Double-1>', self.deleteSelected)  # Double-1 can be reassigned
        #    for diagnostic reasons so you don't need to create a new widget to test a function.
        self.tbl.grid(sticky='nsew', columnspan=6)
        self.treeScroll.grid(row=0, column=6, sticky='ns')
        self.treeview = self.tbl
        Separator(self, orient='horizontal').grid(row=1,
                                                  columnspan=6, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        id = 1

    def createEntry(self):
        '''
        Create the entry fields to input data into the log
        '''

        self.dateLbl = Label(self, text="Enter Date:")
        self.dateEntry = Entry(self)
        self.odoLbl = Label(self, text="Odometer:")
        self.odoEntry = Entry(self)
        self.tripLbl = Label(self, text="Tripometer:")
        self.tripEntry = Entry(self)
        self.galLbl = Label(self, text="Gallons:")
        self.galEntry = Entry(self)
        self.ppgLbl = Label(self, text="Price/Gallon:")
        self.ppgEntry = Entry(self)
        self.totalLbl = Label(self, text="Total:")
        self.totalEntry = Entry(self)
        self.submit = Button(self, text="Submit", command=self.insertData) # command needs to insert field imputs into the Treeview
        self.delete = Button(self, text="Delete", command=self.deleteSelected)
        self.qt = Button(self, text="Quit", command=self.controller.quit)

        self.dateLbl.grid(row=2, column=0, sticky='e')
        self.dateEntry.grid(row=2, column=1)
        self.odoLbl.grid(row=2, column=2)
        self.odoEntry.grid(row=2, column=3)
        self.tripLbl.grid(row=2, column=4)
        self.tripEntry.grid(row=2, column=5)

        self.galLbl.grid(row=3, column=0, sticky='e')
        self.galEntry.grid(row=3, column=1)
        self.ppgLbl.grid(row=3, column=2)
        self.ppgEntry.grid(row=3, column=3)
        self.totalLbl.grid(row=3, column=4)
        self.totalEntry.grid(row=3, column=5)

        self.qt.grid(row=4, column=0, columnspan=2, sticky='w')
        self.delete.grid(row=4, column=4, sticky='e')
        self.submit.grid(row=4, column=5, columnspan=1, sticky='w')

    def insertData(self):
        '''
        Insert data from entry fields into Treeview, as well as save the data
        to an external CSV file
        '''
        self.tbl.insert('', 'end', text="No_"+str(self.id),
                             values=(self.dateEntry.get(), self.odoEntry.get(),
                                     self.tripEntry.get(), self.galEntry.get(),
                                     self.ppgEntry.get(), self.totalEntry.get()))
        with open('%s/fillupLogDat.csv' % self.path, 'a') as f:
            cWriter = csv.writer(f)
            cWriter.writerow([
                "No_"+str(self.id),self.dateEntry.get(), self.odoEntry.get(),
                self.tripEntry.get(), self.galEntry.get(), self.ppgEntry.get(),
                self.totalEntry.get()
            ])
        self.clearFields()
        self.id += 1

    def loadData(self):
        '''
        Load all previously saved entries when application starts
        '''
        self.id = 1
        try:
            load = open('%s/fillupLogDat.csv' % self.path, 'r')
            cReader = csv.reader(load)
            for row in cReader:
                self.tbl.insert('', 'end', text="No_"+str(self.id), values=(
                    row[1], row[2], row[3], row[4], row[5], row[6]
                ))
                self.id += 1
            load.close()
        except FileNotFoundError:
            pass

    def selectItem(self,a):
        '''inserts the values of a selected row 'back' into the entry fields
        for editing
        '''
        try:
            self.clearFields()
            curItem = self.tbl.focus()
            row = self.tbl.item(curItem)['values']
            self.dateEntry.insert(0, row[0])
            self.odoEntry.insert(0, row[1])
            self.tripEntry.insert(0, row[2])
            self.galEntry.insert(0, row[3])
            self.ppgEntry.insert(0, row[4])
            self.totalEntry.insert(0, row[5])
        except IndexError:
            pass

    def clearFields(self):
        '''
        clear all entry fields after insert or delete
        '''
        self.entryFields = (self.dateEntry, self.odoEntry, self.tripEntry,
                            self.galEntry, self.ppgEntry, self.totalEntry)
        for item in self.entryFields:
            item.delete('0', 'end')

    def deleteSelected(self):
        '''
        delete the selected entry from both the table and CSV file
        '''
        selected_item = self.tbl.selection()[0]
        child = self.tbl.item(selected_item)['text']
        self.tbl.delete(selected_item)
        self.clearFields()
        with open('%s/fillupLogDat.csv' % self.path, 'r') as inp, open('%s/out_fillup.csv' % self.path, 'w') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                if row[0] != child:
                    writer.writerow(row)
        os.rename('out_fillup.csv', 'fillupLogDat.csv')


# Runner
if __name__ == '__main__':
    app = App()
    app.mainloop()

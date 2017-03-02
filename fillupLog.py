from tkinter import *
from tkinter.ttk import *
import csv

##############TODO###############################TODO#################
# REFACTOR as much as I can
# Research making my app a 'finished project'
# Add a button to delete a selected entry
#     * that means I need to make it so i can select a row to delete
#       by clicking on it then clicking 'delete'
# Clear all entry fields after 'submit' is pressed
# load row data into entry fields when (row) clicked on for editing
#     * maybe make an edit button instead to prevent accidental editing
# add some color/styling
#     * alternate bg color of rows
#     * play with padding/sticky etc to get a cleaner look
##############TODO###############################TODO##################

class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # not needed until multiple pages

        frame = GasLog(container, self)
        self.frames[GasLog] = frame
        frame.grid(sticky='nsew')

        self.show_frame(GasLog)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GasLog(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # initialize all pieces of a 'page' which are all defined as functions
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
        self.tbl.heading("#0", text="No.", anchor='w')
        self.tbl.column("#0", anchor='w', width=75)
        for n in self.tbl['columns']:
            self.tbl.heading(n, text=n)
            self.tbl.column(n, width=100)
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
        self.qt = Button(self, text="Quit", command=self.controller.quit)

        self.dateLbl.grid(row=2, column=0)
        self.dateEntry.grid(row=2, column=1)
        self.odoLbl.grid(row=2, column=2)
        self.odoEntry.grid(row=2, column=3)
        self.tripLbl.grid(row=2, column=4)
        self.tripEntry.grid(row=2, column=5)

        self.galLbl.grid(row=3, column=0)
        self.galEntry.grid(row=3, column=1)
        self.ppgLbl.grid(row=3, column=2)
        self.ppgEntry.grid(row=3, column=3)
        self.totalLbl.grid(row=3, column=4)
        self.totalEntry.grid(row=3, column=5)

        self.qt.grid(row=4, column=0, columnspan=2, sticky='w')
        self.submit.grid(row=4, column=5, columnspan=2, sticky='e')

    def insertData(self):
        self.tbl.insert('', 'end', text="No_"+str(self.id),
                             values=(self.dateEntry.get(), self.odoEntry.get(),
                                     self.tripEntry.get(), self.galEntry.get(),
                                     self.ppgEntry.get(), self.totalEntry.get()))
        with open('fillupLogDat.csv', 'a') as f:
            cWriter = csv.writer(f)
            cWriter.writerow([
                self.dateEntry.get(), self.odoEntry.get(), self.tripEntry.get(),
                self.galEntry.get(), self.ppgEntry.get(), self.totalEntry.get()
            ])
        self.id += 1

    def loadData(self):
        self.id = 1
        try:
            load = open('fillupLogDat.csv', 'r')
            cReader = csv.reader(load)
            for row in cReader:
                self.tbl.insert('', 'end', text="No_"+str(self.id), values=(
                    row[0], row[1], row[2], row[3], row[4], row[5]
                ))
                self.id += 1
            load.close()
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    app = App()
    app.mainloop()

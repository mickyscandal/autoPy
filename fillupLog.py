from tkinter import *
from tkinter.ttk import *
import csv

##############TODO###############################TODO#################
# CREATE loadData() to initialize past log entries
# REFACTOR as much as I can
# Research making my app a 'finished project'
#
#
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
        self.datFile = open('gasLogDat.csv', 'a')
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

        self.tbl = Treeview(self)  # height=30 ??
        self.treeScroll = Scrollbar(self, orient='vertical',
                                    command=self.tbl.yview)
        self.treeScroll.configure(command=self.tbl.yview)
        self.tbl.configure(yscrollcommand=self.treeScroll.set)
        self.tbl['columns'] = ('date', 'odometer', 'tripometer', 'gallons', 'ppg', 'total')
        self.tbl.heading("#0", text="No.", anchor='w')
        self.tbl.column("#0", anchor='w', width=75)
        for n in self.tbl['columns']:
            self.tbl.heading(n, text=n)
            self.tbl.column(n, width=100)
        self.tbl.grid(sticky='nsew', columnspan=6)
        self.treeScroll.grid(row=0, column=6, sticky='ns')
        self.treeview = self.tbl
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
        self.qt = Button(self, text="Quit", command=self.exit)

        self.dateLbl.grid(row=1, column=0)
        self.dateEntry.grid(row=1, column=1)
        self.odoLbl.grid(row=1, column=2)
        self.odoEntry.grid(row=1, column=3)
        self.tripLbl.grid(row=1, column=4)
        self.tripEntry.grid(row=1, column=5)

        self.galLbl.grid(row=2, column=0)
        self.galEntry.grid(row=2, column=1)
        self.ppgLbl.grid(row=2, column=2)
        self.ppgEntry.grid(row=2, column=3)
        self.totalLbl.grid(row=2, column=4)
        self.totalEntry.grid(row=2, column=5)

        self.qt.grid(row=3, column=0, columnspan=2, sticky='w')
        self.submit.grid(row=3, column=5, columnspan=2, sticky='e')
        self.id = 1

    def insertData(self):
        self.tbl.insert('', 'end', text="No_"+str(self.id),
                             values=(self.dateEntry.get(), self.odoEntry.get(),
                                     self.tripEntry.get(), self.galEntry.get(),
                                     self.ppgEntry.get(), self.totalEntry.get()))
        cWriter = csv.writer(self.datFile)
        cWriter.writerow([
            self.dateEntry.get(), self.odoEntry.get(), self.tripEntry.get(),
            self.galEntry.get(), self.ppgEntry.get(), self.totalEntry.get()
        ])
        self.id += 1

    def loadData(self):
        pass

    def exit(self):
        self.datFile.close()
        self.controller.quit()




if __name__ == '__main__':
    app = App()
    app.mainloop()

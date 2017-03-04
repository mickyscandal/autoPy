import csv
import os
from tkinter import *
from tkinter.ttk import *

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
        self.createTable()
        self.createEntry()


    def createTable(self):

        self.tv = Treeview(self)
        self.tv['columns'] = ('one', 'two', 'three')
        for name in self.tv['columns']:
            self.tv.heading(name, text=name)
            self.tv.column(name, width=100)
        self.tv.grid(sticky='nsew', columnspan=6)
        self.tv.bind('<ButtonRelease-1>', self.showStuff)

    def createEntry(self):
        onelbl = Label(self, text='one:')
        self.oneentry = Entry(self)
        twolbl = Label(self, text='two')
        self.twoentry = Entry(self)
        threelbl = Label(self, text='three')
        self.threeentry = Entry(self)
        self.sbmt = Button(self, text='submit', command=self.insertData)

        onelbl.grid(row=1, column=0)
        self.oneentry.grid(row=1, column=1)
        twolbl.grid(row=1, column=2)
        self.twoentry.grid(row=1, column=3)
        threelbl.grid(row=1, column=4)
        self.threeentry.grid(row=1, column=5)
        self.sbmt.grid(row=2, column=0)

    def insertData(self):
        self.tv.insert('', 'end', text='test', values=(
            self.oneentry.get(), self.twoentry.get(), self.threeentry.get()
        ))

    def showStuff(self,a):
        children = self.tv.get_children()
        print(children)


if __name__ == '__main__':
    app = App()
    app.mainloop()

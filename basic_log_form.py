from tkinter import *
from tkinter.ttk import *
import datetime

LARGE_FONT = ("Verdana", 20)

CONSTRUCTION = 'This app is still under development, check back soon!'

TIMESTAMP = datetime.datetime.today().strftime("%m/%d/%Y")

class AutoLogApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self, relief=RIDGE, borderwidth=3)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SplashPage, GasLog):              ## PAGE CLASSES NEED TO BE LISTED HERE

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(SplashPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SplashPage(Frame):
    '''Application start page

    This is the applications default page, when you open the app this screen appears first
    '''
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        header = Frame(self, relief='ridge', borderwidth=3)
        header.grid(row=0, column=0, columnspan=2, sticky='nsew')

        welcomeLbl = Label(header, text="Welcome to AutoPy!", font=LARGE_FONT)
        welcomeLbl.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        noteLbl = Label(header, text=CONSTRUCTION)
        noteLbl.grid(row=1, column=0)

        button1 = Button(self, text="Preview App (gas log)",
                            command=lambda: controller.show_frame(GasLog))
        button1.grid(row=1, column=0)

        button2 = Button(self, text="Quit",
                            command=parent.quit)
        button2.grid(row=1, column=1)



# I REALLY NEED TO CLEAN THIS CLASS/METHODS UP. THERE'S NO REASON I SHOULD BE REPEATING
# MYSELF THIS MUCH.
class GasLog(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.createLog()
        # self.loadLog()
        self.grid(sticky='nsew')

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
        self.qt = Button(self, text="Quit", command=parent.quit)

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

    def createLog(self):
        self.tbl = Treeview(self)  # height=30 ??
        self.treeScroll = Scrollbar(self, orient='vertical',
                                    command=self.tbl.yview)
        self.treeScroll.configure(command=self.tbl.yview)
        self.tbl.configure(yscrollcommand=self.treeScroll.set)
        self.tbl['columns'] = ('date', 'odometer', 'tripometer', 'gallons', 'ppg', 'total')
        self.tbl.heading("#0", text="No.", anchor='w')
        self.tbl.column("#0", anchor='w', width=75)
        self.tbl.heading('date', text="Date")
        self.tbl.column('date', anchor='center', width=100)
        self.tbl.heading('odometer', text="Odometer")
        self.tbl.column('odometer', anchor='center', width=100)
        self.tbl.heading('tripometer', text="Tripometer")
        self.tbl.column('tripometer', anchor='center', width=100)
        self.tbl.heading('gallons', text="Gallons")
        self.tbl.column('gallons', anchor='center', width=100)
        self.tbl.heading('ppg', text="Price/Gallon")
        self.tbl.column('ppg', anchor='center', width=100)
        self.tbl.heading('total', text="Total")
        self.tbl.column('total', anchor='center', width=100)
        self.tbl.grid(sticky='nsew', columnspan=6)
        self.treeScroll.grid(row=0, column=6, sticky='ns')
        self.treeview = self.tbl
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.id = 1

    def insertData(self):
        self.treeview.insert('', 'end', text="No_"+str(self.id),
                             values=(self.dateEntry.get(), self.odoEntry.get(),
                                     self.tripEntry.get(), self.galEntry.get(),
                                     self.ppgEntry.get(), self.totalEntry.get()))
        self.id += 1


if __name__ =="__main__":
    app = AutoLogApp()
    app.mainloop()

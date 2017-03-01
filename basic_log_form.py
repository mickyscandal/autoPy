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


class GasLog(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.createLog()
        self.loadLog()
        self.grid(sticky='nsew')
        dateLbl = Label(self, text="Enter Date:")
        dateEntry = Entry(self)

        odoLbl = Label(self, text="Odometer:")
        odoEntry = Entry(self)

        dateLbl.grid(row=1, column=0)
        dateEntry.grid(row=1, column=1)

        odoLbl.grid(row=1, column=2)
        odoEntry.grid(row=1, column=3)

        # homeBtn = Button(self, text="back home",
        #                 command=lambda: controller.show_frame(SplashPage))
        # homeBtn.grid(row=1, column=0, sticky="nsew")

    def createLog(self):
        tbl = Treeview(self)  # height=30 ??
        tbl['columns'] = ('date', 'odometer', 'tripometer', 'gallons', 'ppg', 'total')
        tbl.heading("#0", text="No.", anchor='w')
        tbl.column("#0", anchor='w', width=75)
        tbl.heading('date', text="Date")
        tbl.column('date', anchor='center', width=100)
        tbl.heading('odometer', text="Odometer")
        tbl.column('odometer', anchor='center', width=100)
        tbl.heading('tripometer', text="Tripometer")
        tbl.column('tripometer', anchor='center', width=100)
        tbl.heading('gallons', text="Gallons")
        tbl.column('gallons', anchor='center', width=100)
        tbl.heading('ppg', text="Price/Gallon")
        tbl.column('ppg', anchor='center', width=100)
        tbl.heading('total', text="Total")
        tbl.column('total', anchor='center', width=100)
        tbl.grid(sticky='nsew', columnspan=4)
        self.treeview = tbl
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.id = 1

    def loadLog(self):
        self.treeview.insert('', 'end', text="No. "+str(self.id), values=('100,000',
                    '300.00', '11.05', '$2.45', '$27.07'))
        self.treeview.insert('', 'end', text=TIMESTAMP, values=('is',
                    'some', 'more'))
        self.id += 1


if __name__ =="__main__":
    app = AutoLogApp()
    app.mainloop()

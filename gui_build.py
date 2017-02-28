#!/usr/bin/env python3

# AutoPy - Automotive maintenance and fill-up log
# Written by: Micky Scandal   EMAIL: mickyscandal@gmail.com
# VERSION 0.1-A (Python Version: 3.5.2)

from tkinter import *
# from tkinter import ttk

LARGE_FONT = ("Verdana", 20)

CONSTRUCTION = 'This app is still under development, check back soon!'

class AutoLogApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self, relief=RIDGE, borderwidth=3)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SplashPage, MainPage):              ## PAGE CLASSES NEED TO BE LISTED HERE

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

        button1 = Button(self, text="Preview App",
                            command=lambda: controller.show_frame(MainPage))
        button1.grid(row=1, column=0)

        button2 = Button(self, text="Quit",
                            command=parent.quit)
        button2.grid(row=1, column=1)


class MainPage(Frame):
    '''Example for a second page

    Could be another 'tab' or something of the sort (like hitting links in a web
    browser)
    '''
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        ## START EDITING HERE ##
        label = Label(self, text="page one", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = Button(self, text="back to home",
                            command=lambda: controller.show_frame(SplashPage))
        button1.pack()

        ## END EDITING HERE ##



app = AutoLogApp()
app.mainloop()

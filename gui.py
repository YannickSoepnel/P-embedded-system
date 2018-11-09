from tkinter import *
import time

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from test import data
#from connection import connectie1
import threading





class Program:
    style.use('ggplot')

    root = Tk()
    root.title('IT-works')
    main = Frame(bg='grey')
    main.pack(side=TOP)

    status=0
    count = 0

    def __init__(self):

        #connectie1.recieve_data()
        self.handle_click()

        self.Label1 = Label(self.main, text='Temperatuur', fg='black', bg = 'grey')
        self.Label1.grid(row=0, column=0, columnspan=4)
        self.Label2 = Label(self.main, text='Huidige temperatuur: ', fg='black', bg='grey')
        self.Label2.grid(row=1, column=0, columnspan=2)
        self.Label4 = Label(self.main, text='Grens Temperatuur: ', fg='black', bg='grey')
        self.Label4.grid(row=2, column=0, columnspan=2)
        self.Label5 = Label(self.main, text='0', fg='black', bg='grey')
        self.Label5.grid(row=1, column=2, padx=50)
        self.temperatuur = Scale(self.main, orient='horizontal', from_=-20, to=50, length=200, command= self.temperatuur)
        self.temperatuur.set(20)
        self.temperatuur.grid(row=4, column=1, columnspan=2)



        self.Label10 = Label(self.main, text='Licht intensiteit', fg='black', bg='grey')
        self.Label10.grid(row=0, column=4, columnspan=2)
        self.Label12 = Label(self.main, text='Huidige licht intensiteit: ', fg='black', bg='grey')
        self.Label12.grid(row=1, column=3, columnspan=2, padx=50)
        self.Label14 = Label(self.main, text='Grens licht intensiteit: ', fg='black', bg='grey')
        self.Label14.grid(row=2, column=3, columnspan=2)
        self.Label15 = Label(self.main, text='0', fg='black', bg='grey')
        self.Label15.grid(row=1, column=5, padx=50)
        self.licht = Scale(self.main, orient='horizontal', from_=0.1, to=130000, length=200, command=self.licht)
        self.licht.set(1000)
        self.licht.grid(row=4, column=4, columnspan=2)

        self.Label16 = Label(self.main, text='Status', fg='black', bg='grey')
        self.Label16.grid(row=0, column=8, columnspan=2)
        self.button = Button(self.main, width=10, height=2, text="Uitrollen", fg="black", command=self.uitrollen)
        self.button.grid(row=1, column=8)
        self.button2 = Button(self.main, width=10, height=2, text="Inrollen", fg="black", command=self.inrollen)
        self.button2.grid(row=1, column=9)

        self.quitButton = Button(self.main, text='Quit App', width=10, height=2, command=quit)
        self.quitButton.grid(row=1, column=10)


        self.Label17 = Label(self.main, text='Temperatuur', fg='black', bg = 'grey')
        self.Label17.grid(row=5, column=0, columnspan=4, pady=30)
        self.show_graph()

        self.Label18 = Label(self.main, text='Licht intensiteit', fg='black', bg = 'grey')
        self.Label18.grid(row=5, column=4, columnspan=4, pady=30)
        self.show_graph2()

        self.Label19 = Label(self.main, text='Derde grafiek', fg='black', bg = 'grey')
        self.Label19.grid(row=5, column=8, columnspan=4, pady=30)
        self.show_graph3()

        self.Label20 = Label(self.main, text='Vierde grafiek', fg='black', bg = 'grey')
        self.Label20.grid(row=7, column=0, columnspan=4, pady=30)
        self.show_graph4()

        self.Label21 = Label(self.main, text='Vijfde grafiek', fg='black', bg = 'grey')
        self.Label21.grid(row=7, column=4, columnspan=4, pady=30)
        self.show_graph5()

        self.button = Button(self.main, text="Klik voor info", command=self.create_window)
        self.button.grid(row=4, column=6)

        self.update = Button(self.main, text="Update", width=10, height=1, command=self.handle_click)
        self.update.grid(row=4, column=7)


    def create_window(self):
        top = Toplevel(bg='grey')
        top.title("Info")


        Label1 = Label(top, text='Zonlicht:', bg='grey')
        Label1.grid(row=2, column=1)
        label11 = Label(top, text='100 000 - 130 000 lux', bg='grey')
        label11.grid(row=2, column=2)

        Label2 = Label(top, text='Daglicht, indirect zonlicht:', bg='grey')
        Label2.grid(row=3, column=1)
        Label22 = Label(top, text='10 000 - 20 000 lux', bg='grey')
        Label22.grid(row=3, column=2)

        Label3 = Label(top, text='Bewolkte dag:', bg='grey')
        Label3.grid(row=4, column=1)
        Label33 = Label(top, text='1000 lux', bg='grey')
        Label33.grid(row=4, column=2)

        Label4 = Label(top, text='Kantoor:', bg='grey')
        Label4.grid(row=5, column=1)
        Label44 = Label(top, text='500 lux', bg='grey')
        Label44.grid(row=5, column=2)

        Label5 = Label(top, text='Erg donkere dag: ', bg='grey')
        Label5.grid(row=6, column=1)
        Label55 = Label(top, text='100 lux', bg='grey')
        Label55.grid(row=6, column=2)

        Label6 = Label(top, text='Schemering:', bg='grey')
        Label6.grid(row=7, column=1)
        Label66 = Label(top, text='10 lux', bg='grey')
        Label66.grid(row=7, column=2)

        Label7 = Label(top, text='Donkere schemering:', bg='grey')
        Label7.grid(row=8, column=1)
        Label77 = Label(top, text='1 lux', bg='grey')
        Label77.grid(row=8, column=2)

        button = Button(top, text="Exit info", width=10, height=1, command=top.destroy)
        button.grid(row=9, column=1)


    def handle_click(self):
        win = Toplevel()
        win.transient()
        Label(win, text='Please wait...').pack()
        i = 5
        def callback():
            nonlocal i, win
            print(i)
            i -= 1
            if not i:
                win.destroy()
                self.handle_click()
            else:
               self.root.after(1000, callback)
        self.root.after(1000, callback)

    def temperatuur(self, temp):
        self.Label3 = Label(self.main, text=temp, fg='black', bg='grey')
        self.Label3.grid(row=2, column=2)
        print("Tempratuur: " + temp)

    def licht(self, lux):
        self.Label13 = Label(self.main, text=lux, fg='black', bg='grey')
        self.Label13.grid(row=2, column=5)
        print("Lux: " + lux)

    def inrollen(self):
        connectie1.senddata(0xff)
        status = 1
        if (status == 1):
            Label22 = Label(self.main, text='Ingerold', fg='red', bg='grey')
            Label22.grid(row=4, column=8, columnspan=2)

    def uitrollen(self):
        connectie1.senddata(0x0f)
        status = 0
        if (status == 0):
            Label22 = Label(self.main, text='Uitgerold', fg='green', bg='grey')
            Label22.grid(row=4, column=8, columnspan=2)



    def show_graph(self):

        self.x = data.listx
        self.y = data.listy

        figure = Figure(figsize=(4,4), dpi=70)

        a = figure.add_subplot(111)
        a.plot(self.x,self.y,marker='o')
        a.grid()

        canvas = FigureCanvasTkAgg(figure, master=self.main)
        canvas.draw()

        graph_widget = canvas.get_tk_widget()
        graph_widget.grid(row=6,column=1,columnspan=2, padx=80, sticky='nsew')

    def show_graph2(self):

        self.x = data.listx
        self.y = data.listy

        figure1 = Figure(figsize=(4, 4), dpi=70)

        aa = figure1.add_subplot(111)
        aa.plot(self.x, self.y, marker='o')
        aa.grid()

        canvas1 = FigureCanvasTkAgg(figure1, master=self.main)
        canvas1.draw()

        graph_widget1 = canvas1.get_tk_widget()
        graph_widget1.grid(row=6, column=4, columnspan=2,sticky='nsew', padx=80)

    def show_graph3(self):

        self.x = data.listx
        self.y = data.listy

        figure1 = Figure(figsize=(4, 4), dpi=70)

        aa = figure1.add_subplot(111)
        aa.plot(self.x, self.y, marker='o')
        aa.grid()

        canvas1 = FigureCanvasTkAgg(figure1, master=self.main)
        canvas1.draw()

        graph_widget1 = canvas1.get_tk_widget()
        graph_widget1.grid(row=6, column=8, columnspan=3,sticky='nsew', padx=80)

    def show_graph4(self):

        self.x = data.listx
        self.y = data.listy

        figure1 = Figure(figsize=(4, 4), dpi=70)

        aa = figure1.add_subplot(111)
        aa.plot(self.x, self.y, marker='o')
        aa.grid()

        canvas1 = FigureCanvasTkAgg(figure1, master=self.main)
        canvas1.draw()

        graph_widget1 = canvas1.get_tk_widget()
        graph_widget1.grid(row=8, column=1, columnspan=2,sticky='nsew', padx=80)

    def show_graph5(self):

        self.x = data.listx
        self.y = data.listy

        figure1 = Figure(figsize=(4, 4), dpi=70)

        aa = figure1.add_subplot(111)
        aa.plot(self.x, self.y, marker='o')
        aa.grid()

        canvas1 = FigureCanvasTkAgg(figure1, master=self.main)
        canvas1.draw()

        graph_widget1 = canvas1.get_tk_widget()
        graph_widget1.grid(row=8, column=4, columnspan=3,sticky='nsew', padx=80)


program = Program()

mainloop()

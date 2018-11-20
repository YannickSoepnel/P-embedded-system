from tkinter import *
from tkinter import ttk
import threading
import time



class gui:
    title = "Sunscreen"
    root = None
    main = Frame()
    main.pack(side=TOP)
    rate = 60


    def build(self):
        root = Tk()

        self.root = root
        root.title(self.title)
        root.mainloop()


    def labels_buttons(self):
        self.tempratuurlabel = Label(self.main, text='Temperatuur', fg='black')
        self.tempratuurlabel.grid(row=0, column=0, columnspan=4)
        self.huidigetemp = Label(self.main, text='Huidige temperatuur: ', fg='black')
        self.huidigetemp.grid(row=1, column=0, columnspan=2)
        self.grenstemp = Label(self.main, text='Grens Temperatuur: ', fg='black', anchor='w')
        self.grenstemp.grid(row=2, column=0, columnspan=2)
        self.temperatuur = Scale(self.main, orient='horizontal', from_=-20, to=50, length=200)
        self.temperatuur.set(30)
        self.temperatuur.grid(row=4, column=1, columnspan=2)

        self.lichtlabel = Label(self.main, text='Licht intensiteit', fg='black')
        self.lichtlabel.grid(row=0, column=4, columnspan=2)
        self.huidiglicht = Label(self.main, text='Huidige licht intensiteit: ', fg='black')
        self.huidiglicht.grid(row=1, column=3, columnspan=2, padx=50)
        self.grenslicht = Label(self.main, text='Grens licht intensiteit: ', fg='black')
        self.grenslicht.grid(row=2, column=3, columnspan=2)
        self.licht = Scale(self.main, orient='horizontal', from_=0, to=165, length=200)
        self.licht.set(130)
        self.licht.grid(row=4, column=4, columnspan=2)


        self.Status = Label(self.main, text='Status', fg='black')
        self.Status.grid(row=5, column=6, columnspan=2)
        self.quitButton = Button(self.main, text='Quit App', width=10, height=2, command=quit)
        self.quitButton.grid(row=1, column=8)
        self.Label17 = Label(self.main, text='Temperatuur', fg='black')
        self.Label17.grid(row=5, column=0, columnspan=4, pady=30)
        self.Label18 = Label(self.main, text='Licht intensiteit', fg='black')
        self.Label18.grid(row=5, column=4, columnspan=4, pady=30)
        self.afstand1 = Label(self.main, text='Afstand: ', fg='black')
        self.afstand1.grid(row=1, column=5, columnspan=2)



if __name__ == '__main__':
    mainloop()
from tkinter import *
import time

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import serial
import struct


lichtser = serial.Serial('COM9',19200)             # Open connectie op COM6
temperatuurser = serial.Serial('COM10', 19200)      # Open connectie op COM10
# afstandser = serial.Serial('COM3',19200)
# ser = serial.Serial('/dev/tty.usbmodem1411', 19200)

class Program:
    style.use('ggplot')

    root = Tk()
    root.title('IT-works')
    main = Frame(bg='grey')
    main.pack(side=TOP)

    status = 0
    count = 0

    countx_temperatuur = 0
    countx_licht = 0
    countx_temperatuur_lijst = []
    countx_licht_lijst = []
    temperatuur_data = []
    licht_data = []
    afstand_data = []
    afstand_rolluik = 90
    uitrollen_status = 0
    groen = 0
    geel = 0
    rood = 0xff
    lichtgrens = 130
    tempgrens = 30

    temperatuur_last = temperatuur_data[-1:]
    licht_last = licht_data[-1:]

    def __init__(self):

        #connectie1.recieve_data()
        self.handle_click()
        # .write(struct.pack('>B', self.rood))

        self.Label1 = Label(self.main, text='Temperatuur', fg='black', bg = 'grey')
        self.Label1.grid(row=0, column=0, columnspan=4)
        self.Label2 = Label(self.main, text='Huidige temperatuur: ', fg='black', bg='grey')
        self.Label2.grid(row=1, column=0, columnspan=2)
        self.Label4 = Label(self.main, text='Grens Temperatuur: ', fg='black', bg='grey')
        self.Label4.grid(row=2, column=0, columnspan=2)
        self.Label5 = Label(self.main, text='0', fg='black', bg='grey')
        self.Label5.grid(row=1, column=2, padx=50)
        self.temperatuur = Scale(self.main, orient='horizontal', from_=-20, to=50, length=200, command= self.temperatuur)
        self.temperatuur.set(30)
        self.temperatuur.grid(row=4, column=1, columnspan=2)



        self.Label10 = Label(self.main, text='Licht intensiteit', fg='black', bg='grey')
        self.Label10.grid(row=0, column=4, columnspan=2)
        self.Label12 = Label(self.main, text='Huidige licht intensiteit: ', fg='black', bg='grey')
        self.Label12.grid(row=1, column=3, columnspan=2, padx=50)
        self.Label14 = Label(self.main, text='Grens licht intensiteit: ', fg='black', bg='grey')
        self.Label14.grid(row=2, column=3, columnspan=2)
        self.licht = Scale(self.main, orient='horizontal', from_=0, to=165, length=200, command=self.licht)
        self.licht.set(130)
        self.licht.grid(row=4, column=4, columnspan=2)

        self.Label16 = Label(self.main, text='Status', fg='black', bg='grey')
        self.Label16.grid(row=5, column=6, columnspan=2)
        self.button = Button(self.main, width=10, height=2, text="Uitrollen", fg="black", command=self.uitrollen)
        self.button.grid(row=4, column=7)
        self.button2 = Button(self.main, width=10, height=2, text="Inrollen", fg="black", command=self.inrollen)
        self.button2.grid(row=4, column=8)

        self.quitButton = Button(self.main, text='Quit App', width=10, height=2, command=quit)
        self.quitButton.grid(row=1, column=8)


        self.Label17 = Label(self.main, text='Temperatuur', fg='black', bg = 'grey')
        self.Label17.grid(row=5, column=0, columnspan=4, pady=30)

        self.Label18 = Label(self.main, text='Licht intensiteit', fg='black', bg = 'grey')
        self.Label18.grid(row=5, column=4, columnspan=4, pady=30)

        self.create_window = Button(self.main, text="Licht info", command=self.create_window)
        self.create_window.grid(row=4, column=6)


        self.afstand1 = Label(self.main, text='Afstand: ', fg='black', bg='grey')
        self.afstand1.grid(row=1, column=5, columnspan=2)

    def create_window(self):
        top = Toplevel(bg='grey')
        top.title("Info")


        Label1 = Label(top, text='Zonlicht:', bg='grey')
        Label1.grid(row=2, column=1)
        label11 = Label(top, text='165', bg='grey')
        label11.grid(row=2, column=2)

        Label2 = Label(top, text='Daglicht, indirect zonlicht:', bg='grey')
        Label2.grid(row=3, column=1)
        Label22 = Label(top, text='150', bg='grey')
        Label22.grid(row=3, column=2)

        Label3 = Label(top, text='Bewolkte dag:', bg='grey')
        Label3.grid(row=4, column=1)
        Label33 = Label(top, text='140', bg='grey')
        Label33.grid(row=4, column=2)

        Label4 = Label(top, text='Kantoor:', bg='grey')
        Label4.grid(row=5, column=1)
        Label44 = Label(top, text='120', bg='grey')
        Label44.grid(row=5, column=2)

        Label5 = Label(top, text='Erg donkere dag: ', bg='grey')
        Label5.grid(row=6, column=1)
        Label55 = Label(top, text='100', bg='grey')
        Label55.grid(row=6, column=2)

        Label6 = Label(top, text='Schemering:', bg='grey')
        Label6.grid(row=7, column=1)
        Label66 = Label(top, text='80', bg='grey')
        Label66.grid(row=7, column=2)

        Label7 = Label(top, text='Donkere schemering:', bg='grey')
        Label7.grid(row=8, column=1)
        Label77 = Label(top, text='40', bg='grey')
        Label77.grid(row=8, column=2)

        button = Button(top, text="Exit info", width=10, height=1, command=top.destroy)
        button.grid(row=9, column=1)


    def handle_click(self):
        i = 5
        def callback():
            nonlocal i
            i -= 1
            if not i:
                # Hier staan alle functies die telkens uitgevoerd moeten worden
                self.handle_click()
                self.update_data()
                self.afstand_meten_uitrollen()
                self.afstand_meten_inrollen()
                self.temperatuur_graph()
                self.licht_graph()
                #self.data_afstand()
                self.updatelabels()
                self.check_licht()
            else:
               self.root.after(50, callback)
        self.root.after(50, callback)

    def check_licht(self):
        laatste_licht = self.licht_data[-1]     # Zet de laatste waargenomen lichtintensiteit in een variabele
        if int(laatste_licht) > int(self.lichtgrens) and self.uitrollen_status == 0:
            # Kijk of die waarde boven de grens van lichtintensiteit ligt
            # Als dit zo is, rol je de zonneluik uit
            self.uitrollen_arduino()
            self.uitgerold()



    def update_data(self):
        data = self.recieve_data_licht()       # Zet seriële waarde in data
        if data == 0xff:                       # Check of de data 0xff is
            data = self.recieve_data_licht()   # Zet seriële waarde na de 0xff in data
            self.afstand_data.append(data)     # Voeg data toe in de afstand lijst
        data = self.recieve_data_licht()
        if data == 0x0f:                       # Check of de data 0x0f is
            data = self.recieve_data_licht()   # Zet seriële waarde na de 0x0f in data
            self.licht_data.append(data)       # Voeg data toe in de lichtintensiteit lijst
        data = self.recieve_data_temp()
        if data == 0xff:                        # Kijk of de data 0xff is
            data = self.recieve_data_temp()     # Zet seriële waarde na 0xff in data
            data = data / 10                    # Deel de data door 10 omdat hij vanuit de arduino met 10 is vermenigvuldigd
            self.temperatuur_data.append(data)  # Voeg de data toe in de temperatuur lijst

    def recieve_data_licht(self):
        data = lichtser.read().hex()    # zet de data van de poort in een variabele
        data = int(data, 16)            # zet de hexadecimale data om in een integer
        return data


    def recieve_data_temp(self):

        data = temperatuurser.read().hex()  # zet de data van de poort in een variabele
        data = int(data, 16)                # zet de hexadecimale data om in een integer
        return data


    def updatelabels(self):
        self.Label15 = Label(self.main, text=self.licht_data[-1:], fg='black', bg='grey')
        self.Label15.grid(row=1, column=5, padx=50)
        self.afstand = Label(self.main, text=self.afstand_data[-1:], fg='black', bg='grey')
        self.afstand.grid(row=1, column=6, padx=50)
        self.temperatuur = Label(self.main, text=self.temperatuur_data[-1:], fg='black', bg='grey')
        self.temperatuur.grid(row=1, column=2, padx=50)


    def temperatuur(self, temp):
        self.tempgrens = temp
        self.Label3 = Label(self.main, text=temp, fg='black', bg='grey')
        self.Label3.grid(row=2, column=2)

    def licht(self, lux):
        self.lichtgrens = lux
        self.Label13 = Label(self.main, text=lux, fg='black', bg='grey')
        self.Label13.grid(row=2, column=5)

    def uitrollen_arduino(self):
        # blinking led = 0x0e
        # rode led aan = 0xff
        # groene led aan = 0x0f
        onoff = 0x0f
        self.uitrollen_status = 1
        self.geel = 1 #0x0e
        self.geel = 0x0e
        temperatuurser.write(struct.pack('>B', self.geel))
        self.rood = 0 #0xff
        #stuur naar arduino dat geel ledje moet knipperen
        # lampje.write(struct.pack('>B', onoff))

    def inrollen_arduino(self):
        self.uitrollen_status = 0
        self.geel = 1 #0x0e
        self.geel = 0x0e
        temperatuurser.write(struct.pack('>B', self.geel))
        self.groen = 0 #0x0f

    def afstand_meten_uitrollen(self):
        #als de afstand van de afstand sensor overeen komt met de afstand die hij moet uitgerold zijn dan:
        laatste_afstand = self.afstand_data[-1]
        if(laatste_afstand > self.afstand_rolluik and self.uitrollen_status == 1):
            self.uitgerold()


    def afstand_meten_inrollen(self):
        #Als de afstand van de afstandsensor bij minder dan 10?? komt dan moet geel led uit en rood weer aan
        laatste_afstand = self.afstand_data[-1]
        if(laatste_afstand < 10 and self.uitrollen_status == 0):
            self.ingerold()

    def uitgerold(self):
        #stuur naar arduino dat geel ledje uit moet en groene aan moet
        self.geel = 0 #0x0e
        self.groen = 1 #0x0f
        self.groen = 0x0f
        temperatuurser.write(struct.pack('>B', self.groen))

    def ingerold(self):
        self.geel = 0 #0x0e
        self.rood = 1 #0xff
        self.rood = 0xff
        temperatuurser.write(struct.pack('>B', self.rood))

    def uitrollen(self):        #functie achter de knop
        self.uitrollen_arduino()
        Label22 = Label(self.main, text='Uitgerold', fg='green', bg='grey')
        Label22.grid(row=5, column=8, columnspan=2)

    def inrollen(self):         # functie achter de knop
        self.inrollen_arduino()
        Label22 = Label(self.main, text='Ingerold', fg='red', bg='grey')
        Label22.grid(row=5, column=8, columnspan=2)

    def printing(self):
        print("Geel: ")
        print(self.geel)
        print("Groen: ")
        print(self.groen)
        print("Rood: ")
        print(self.rood)
        print("Status: ")
        print(self.uitrollen_status)

    def update_value(self):
        self.laatste_afstand = 110

    def update_value2(self):
        self.laatste_afstand = 9

    def temperatuur_graph(self):

        self.countx_temperatuur_lijst.append(self.countx_temperatuur)
        self.countx_temperatuur += 1

        self.x = self.countx_temperatuur_lijst[-20:]
        self.y = self.temperatuur_data[-20:]

        #self.x = data.listx
        #self.y = data.listy

        figure = Figure(figsize=(4,4), dpi=70)

        a = figure.add_subplot(111)
        a.plot(self.x,self.y,marker='o')
        a.grid()

        canvas = FigureCanvasTkAgg(figure, master=self.main)
        canvas.draw()

        graph_widget = canvas.get_tk_widget()
        graph_widget.grid(row=6,column=1,columnspan=2, padx=80, sticky='nsew')

    def licht_graph(self):

        self.countx_licht_lijst.append(self.countx_licht)
        self.countx_licht += 1

        self.x = self.countx_licht_lijst[-10:]
        self.y = self.licht_data[-10:]

        # self.x = data.listx
        # self.y = data.listy

        figure1 = Figure(figsize=(4, 4), dpi=70)

        aa = figure1.add_subplot(111)
        aa.plot(self.x, self.y, marker='o')
        aa.grid()

        canvas1 = FigureCanvasTkAgg(figure1, master=self.main)
        canvas1.draw()

        graph_widget1 = canvas1.get_tk_widget()
        graph_widget1.grid(row=6, column=4, columnspan=2,sticky='nsew', padx=80)



program = Program()

mainloop()

from tkinter import *
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from test2 import ReadData
from connection import Connectie


class Main:
    root = Tk()
    root.title('Zeng ltd')
    button_frame = Frame(width=300, height=50)
    button_frame.pack()

    status_color = 'white'

    """STATUS"""
    rol_status = 0
    knop = 0
    licht_status = 0
    temperatuur_status = 0

    """"LEDJES"""
    geel = 0
    rood = 1
    groen = 0

    """GRENZEN"""
    grens_rolluik = 100             #Grens van de afstand van rolluik
    licht_grens = 100               #Grens van de licht intensiteit
    temperatuur_grens = 100         #Grens van de temperatuur

    """VARIABELE SENSOREN"""
    licht_intensiteit = 0           #Dit moet de meest recentelijke waarde worden van de lichtsensor
    temperatuur_intensiteit = 0     #Dit moet de meest recentelijke waarde worden van de temperatuursensor
    afstand_rolluik = 0             #Dit moet de meest recentelijke waarde worden van de afstandsensor


    status_frame = Frame(width=50, height=50)
    status_frame.pack()

    graph_frame = Frame(width=300, height=50)
    graph_frame.pack()

    def __init__(self):
        self.handle_click()
        uitrollen_button = Button(self.button_frame, width=12, height=2, text="UITROLLEN", fg="black", command=self.laten_uitrollen_arduino_button)
        uitrollen_button.grid(row=0, column=0)
        inrollen_button = Button(self.button_frame, width=12, height=2, text="INROLLEN", fg="black", command=self.laten_inrollen_arduino_button)
        inrollen_button.grid(row=0, column=1)
        status_button = Button(self.button_frame, width=12, height=2, text="STATUS", fg="black", command=self.printing)
        status_button.grid(row=0, column=2)

        self.quitButton = Button(self.button_frame,text='Quit App', width=12, height=2, command=quit)
        self.quitButton.grid(row=1, column=1)
        self.inforwindow = Button(self.button_frame, width=12, height=2, text="Click for info", fg="black", command=self.create_window)
        self.inforwindow.grid(row=1, column=0)


        # self.afstand = Scale(self.status_frame, orient='horizontal', from_=0, to=165, length=200, command=self.afstand)
        # self.afstand.set(90)
        # self.afstand.grid(row=2, column=0, columnspan=2)
        self.temperatuur = Scale(self.status_frame, orient='horizontal', from_=-10, to=50, length=200, command=self.grens_temperatuur)
        self.temperatuur.set(20)
        self.temperatuur.grid(row=3, column=0, columnspan=2)
        self.licht = Scale(self.status_frame, orient='horizontal', from_=0, to=165, length=200, command=self.grens_licht)
        self.licht.set(90)
        self.licht.grid(row=4, column=0, columnspan=2)

        self.afstandlabel = Label(self.status_frame, text='Afstand: ', fg='black')
        self.afstandlabel.grid(row=5, column=1, columnspan=2)

        self.temperatuur_graph()
        self.licht_graph()


    def create_window(self):
        top = Toplevel()
        top.title("Info")

        Label1 = Label(top, text='Zonlicht:')
        Label1.grid(row=2, column=1)
        label11 = Label(top, text='165')
        label11.grid(row=2, column=2)

        Label2 = Label(top, text='Daglicht, indirect zonlicht:')
        Label2.grid(row=3, column=1)
        Label22 = Label(top, text='150')
        Label22.grid(row=3, column=2)

        Label3 = Label(top, text='Bewolkte dag:')
        Label3.grid(row=4, column=1)
        Label33 = Label(top, text='140')
        Label33.grid(row=4, column=2)

        Label4 = Label(top, text='Kantoor:')
        Label4.grid(row=5, column=1)
        Label44 = Label(top, text='120')
        Label44.grid(row=5, column=2)

        Label5 = Label(top, text='Erg donkere dag: ')
        Label5.grid(row=6, column=1)
        Label55 = Label(top, text='100')
        Label55.grid(row=6, column=2)

        Label6 = Label(top, text='Schemering:')
        Label6.grid(row=7, column=1)
        Label66 = Label(top, text='80')
        Label66.grid(row=7, column=2)

        Label7 = Label(top, text='Donkere schemering:')
        Label7.grid(row=8, column=1)
        Label77 = Label(top, text='40')
        Label77.grid(row=8, column=2)

        button = Button(top, text="Exit info", width=10, height=1, command=top.destroy)
        button.grid(row=9, column=1)

    def printing(self):
        # print('knop: ' + str(self.knop))
        # print('rol status: ' + str(self.rol_status))
        # print('licht: ' + str(self.licht_status))
        # print('Temp: ' + str(self.temperatuur_status))
        # print('Geel: ' + str(self.geel))
        # print('Groen: ' + str(self.groen))
        # print('Rood: ' + str(self.rood))
        # print(ReadData.count_data)
        # print(ReadData.temperatuur_data)
        pass


    """De twee functies hieronder zijn de in en uitrol functie die worden aangeroepen door de twee knoppen"""
    def laten_uitrollen_arduino_button(self):
        self.rol_status = 1
        if(self.geel == 0 and self.groen == 0):
            self.knop = 1
            self.rood = 0
            self.groen = 0
            self.geel = 1
            Connectie.send_led(Connectie, 0x0e)
            Connectie.send_led(Connectie, 0x0f)

    def laten_inrollen_arduino_button(self):
        if(self.rol_status == 0):
            pass
        elif(self.rol_status == 1):
            self.knop = 0
            self.rol_status = 0
            self.geel = 1
            self.groen = 0
            self.rood = 0
            Connectie.send_led(Connectie, 0x0e)
            Connectie.send_led(Connectie, 0x0f)

    """De twee functies hieronder zijn de in en uitrol functie die worden aangeroepen als de lichtsensor over zijn grens gaat"""

    def laten_uitrollen_arduino_licht(self):
        if(self.groen == 0):
            self.rol_status = 1
            self.licht_status = 1
            self.rood = 0
            self.groen = 0
            self.geel = 1

    def laten_inrollen_arduino_licht(self):
        if(self.rol_status == 0):
            pass
        elif(self.rol_status == 1):
            self.rol_status = 0
            self.licht_status = 0
            self.geel = 1
            self.groen = 0
            self.rood = 0

    """De twee functies hieronder zijn de in en uitrol functie die worden aangeroepen als de temperatuursensor over zijn grens gaat"""

    def laten_inrollen_arduino_temp(self):
        if(self.rol_status == 0):
            pass
        elif(self.rol_status == 1):
            self.rol_status = 0
            self.temperatuur_status = 0
            self.geel = 1
            self.groen = 0
            self.rood = 0
            Connectie.send_led(Connectie, 0x0e)
            Connectie.send_led(Connectie, 0x0f)

    def laten_uitrollen_arduino_temp(self):
        if(self.groen == 0):
            self.rol_status = 1
            self.temperatuur_status = 1
            self.rood = 0
            self.groen = 0
            self.geel = 1
            Connectie.send_led(Connectie, 0x0e)
            Connectie.send_led(Connectie, 0x0f)

    def rollen(self):
        if(self.afstand_rolluik > self.grens_rolluik and self.rol_status == 1):
            self.uitrollen()
        elif(self.afstand_rolluik < 10 and self.rol_status == 0):
            self.inrollen()

    def uitrollen(self):        #Deze functie wordt aangeroepen als de afstand van het rolluik over zijn grens gaat
        self.geel = 0           #(dus als hij helemaal uitgerold is)
        self.rood = 0
        self.groen = 1
        Connectie.send_led(Connectie, 0x0f)
        Connectie.send_led(Connectie, 0x00)



    def inrollen(self):         # Deze functie wordt aangeroepen als de afstand van het rolluik onder zijn grens gaat
        self.geel = 0           # (dus als hij helemaal ingerold is)
        self.geel = 0
        self.groen = 0
        self.rood = 1
        Connectie.send_led(Connectie, 0xff)
        Connectie.send_led(Connectie, 0x0f)


    def handle_click(self):
        i = 5
        def callback():
            nonlocal i
            i -= 1
            if not i:
                ReadData.update_data(ReadData)
                self.update_sensor()
                self.handle_click()
                self.update_label()         #Deze functie update de status van het rolluik (ook niet helemaal van toepassing in uiteindelijke project)
                self.color_update()         #Deze functie update het vakje dat het LEDje simuleert (niet van toepassing in uiteindelijke project)
                self.rollen()               #Het constant checken van de afstand van het rolluik met de aangegeven grens
                self.licht_checken()        #Het constant checken van de lichtsensor
                self.temperatuur_checken()  #Het constant checken van de temperatuursensor
                self.licht_graph()          #laat de licht grafiek updaten
                self.temperatuur_graph()    #laat de temp grafiek updaten
                self.printing()

            else:
                self.root.after(50, callback)
        self.root.after(50, callback)

    def update_label(self):
        self.Label15 = Label(self.status_frame, text='          ', fg=self.status_color, bg=self.status_color)
        self.Label15.grid(row=1, column=5)
        self.Label16 = Label(self.status_frame, text=self.rol_status, fg='black', bg='white')
        self.Label16.grid(row=5, column= 5)
        self.label_afstand = Label(self.status_frame, text='afstand: ' + str(self.afstand_rolluik), fg='black')
        self.label_afstand.grid(row=2, column=5)
        self.label_afstand = Label(self.status_frame, text='temperatuur: ' + str(self.temperatuur_intensiteit), fg='black')
        self.label_afstand.grid(row=3, column=5)
        self.label_licht = Label(self.status_frame, text='licht intens: ' + str(self.licht_intensiteit), fg='black')
        self.label_licht.grid(row=4, column=5)

    def update_sensor(self):
        if(len(ReadData.afstand_data) != 0):
            self.afstand_rolluik = ReadData.afstand_data[-1]
        if (len(ReadData.temperatuur_data) != 0):
            self.temperatuur_intensiteit = ReadData.temperatuur_data[-1]
        if (len(ReadData.licht_data) != 0):
            self.licht_intensiteit = ReadData.licht_data[-1]

    """DEZE FUNCTIE SCHRIJFT DE WAARDE VAN SLIDER NAAR LICHT_GRENS"""

    def grens_licht(self, lux):
        self.licht_grens = int(lux)

    def grens_temperatuur(self, temperatuur):
        self.temperatuur_grens = int(temperatuur)




    """Update de kleur van het vakje dat het LEDje moet simuleren"""
    def color_update(self):
        if(self.geel == 1):
            self.status_color = 'yellow'

        elif(self.rood == 1):
            self.status_color = 'red'

        elif(self.groen == 1):
            self.status_color = 'green'


    """Checkt constant de waarde van de lichtsensor"""

    def licht_checken(self):
        #Als de licht intensiteit groter is dan de grens en het rolluik ingerold is
        if(self.licht_intensiteit > self.licht_grens and self.rol_status == 0):
            self.laten_uitrollen_arduino_licht()
        #Als de licht intensiteit kleiner is dan de grens en het rolluik ingerold is en licht_status == 1 dan inrollen
        #licht_status == 1 zorgt ervoor dat de functie kijkt of het rolluik is uitgerold doordat de grens van de licht intensiteit is overschreden
        #Als het rolluik dus is uitgerold door de licht grens dan zal deze ook weer inrollen als de licht intensiteit onder de grens komt
        #Als het rolluik niet is uitgerold door de licht grens dan zal deze ook niet inrollen als de licht intensiteit onder de grens komt (anders blijft hij namelijk inrollen als je op uitrollen drukt)
        elif(self.licht_intensiteit < self.licht_grens and self.rol_status == 1 and self.knop == 0 and self.licht_status == 1):
            self.laten_inrollen_arduino_licht()

    def temperatuur_checken(self):
        if(self.temperatuur_intensiteit > self.temperatuur_grens and self.rol_status == 0):
            self.laten_uitrollen_arduino_temp()
        #Als de temperatuur  kleiner is dan de grens en het rolluik ingerold is en temperatuur_status == 1 dan inrollen
        #temperatuur_status == 1 zorgt ervoor dat de functie kijkt of het rolluik is uitgerold doordat de grens van de temperatuur is overschreden
        #Als het rolluik dus is uitgerold door de temperatuur grens dan zal deze ook weer inrollen als de temperatuur onder de grens komt
        #Als het rolluik niet is uitgerold door de temperatuur grens dan zal deze ook niet inrollen als de temperatuur onder de grens komt (anders blijft hij namelijk inrollen als je op uitrollen drukt)
        elif(self.temperatuur_intensiteit < self.temperatuur_grens and self.rol_status == 1 and self.knop == 0 and self.temperatuur_status == 1):
            self.laten_inrollen_arduino_temp()

    """"Temperatuur grafiek"""
    def temperatuur_graph(self):
        self.x = ReadData.count_data_temperatuur[-10:]
        self.y = ReadData.temperatuur_data[-10:]

        # x = [1, 2, 3, 4, 5]
        # y = [1, 2, 3, 4, 5]
        # self.x = x
        # self.y = y



        figure = Figure(figsize=(4, 4), dpi=70)
        figure.suptitle('Temperatuur')

        a = figure.add_subplot(111)
        a.plot(self.x, self.y, marker='o')
        a.grid()


        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.draw()

        graph_widget = canvas.get_tk_widget()
        graph_widget.grid(row=5, column=0, columnspan=2, sticky='nsew')

    """"Lichtintens grafiek"""
    def licht_graph(self):
        self.x = ReadData.count_data_licht[-10:]
        self.y = ReadData.licht_data[-10:]
        # print(ReadData.count_data)



        figure = Figure(figsize=(4, 4), dpi=70)
        figure.suptitle('Licht intensiteit')


        a = figure.add_subplot(111)
        a.plot(self.x, self.y, marker='o')
        a.grid()

        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.draw()

        graph_widget = canvas.get_tk_widget()
        graph_widget.grid(row=5, column=2, columnspan=2, sticky='nsew')



main = Main()
Main.root.mainloop()


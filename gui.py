from tkinter import *
import time

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

style.use('ggplot')

root = Tk()                #aanmaken van venster
root.title('Python User Interface')

main = Frame(root)
main.pack(side=TOP)

main2 = Frame(root)
main2.pack()


Label1 = Label(main2, text='IT-Works', fg='black')
Label1.grid(row=0,column=1, columnspan= 4)

def uitrollen():
    status = 0
    if (status == 0):
        Label6 = Label(main2, text='uitgerold', fg='red')
        Label6.grid(row=1, column=5, columnspan=1)

def inrollen():
    status = 1
    if (status == 1):
        Label6 = Label(main2, text='ingerold', fg='green')
        Label6.grid(row=1, column=5, columnspan=1)

Label5 = Label(main2, text='Status: ', fg='black')
Label5.grid(row=1,column=4, columnspan= 1)

button1 = Button(main2,width=10, height=2, text="Uitrollen", fg="black", command=uitrollen)
button1.grid(row=1,column=2)

button2 = Button(main2,width=10, height=2, text="Inrollen", fg="black", command=inrollen)
button2.grid(row=1,column=3)

Label2 = Label(main2, text='Temperatuur \n 0 tot 100 celcius', fg='black')
Label2.grid(row=2,column=0)

temperatuur = Scale(main2, from_=100, to=0)
temperatuur.grid(row=3,column=0)

Label3 = Label(main2, text='Lichtintensiteit \n 0 tot 100', fg='black')
Label3.grid(row=2,column=1)

licht = Scale(main2, from_=100, to=0)
licht.grid(row=3,column=1)

Label4 = Label(main2, text='Lichtintensiteit', fg='black')
Label4.grid(row=2,column=2,columnspan=2)

Label4 = Label(main2, text='Temperatuur', fg='black')
Label4.grid(row=2,column=4,columnspan=2)

button3 = Button(main2, text="EXIT", fg="black",width=10, height=2, command=quit)
button3.grid(row=4,column=1,columnspan=4)


x=list()
y=list()


for i in range(12,23):
    x.append(i)

for i in range(1,12):
    y.append(i)

def plot_graph():
    figure = Figure(figsize=(4,4), dpi=70)

    a = figure.add_subplot(111)
    a.plot(x,y,marker='o')
    a.grid()

    canvas = FigureCanvasTkAgg(figure, master=main2)
    canvas.draw()

    graph_widget= canvas.get_tk_widget()
    graph_widget.grid(row=3,column=2, columnspan=2,sticky='nsew')


xx=list()
yy=list()

for i in range(12,23):
    xx.append(i)

for i in range(1,12):
    yy.append(i)

def plot_graph2():
    figure1 = Figure(figsize=(4,4), dpi=70)

    aa = figure1.add_subplot(111)
    aa.plot(xx,yy,marker='o')
    aa.grid()

    canvas1 = FigureCanvasTkAgg(figure1, master=main2)
    canvas1.draw()

    graph_widget1 = canvas1.get_tk_widget()
    graph_widget1.grid(row=3,column=4, columnspan=3,sticky='nsew')

plot_graph()
plot_graph2()

def grafiek():
    a=24
    b=16
    x.append(a)
    y.append(b)
    plot_graph()

button3 = Button(main2, text="GRAFIEK", fg="black",width=10, height=2, command=grafiek)
button3.grid(row=4,column=2,columnspan=1)

root.mainloop()

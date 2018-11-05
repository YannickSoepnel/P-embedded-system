from tkinter import *
import time
import threading

class ScaleValue:
    def __init__(self):
        self.value1 = None
        self.value2 = None


def tkinter_loop(scale):
    root=Tk()
    root.geometry("500x500")
    root.title("IT Works")



    s1 = Scale(root, from_=-20, to=50, length=600, orient=HORIZONTAL, tickinterval=2.5, command=lambda v: setattr(scale, 'value1', v))
    s1.set(10)
    s1.pack()

    s2 = Scale(root, from_=-20, to=50, length=600, orient=HORIZONTAL, tickinterval=2.5, command=lambda v: setattr(scale, 'value2', v))
    s2.set(20)
    s2.pack()

    quitbutton = Button(root, text='quit', command=root.quit)
    quitbutton.pack(side=BOTTOM)

    temp = Label(root, text='Tempratuur: {}'.format(s1.get()))
    temp.pack()

    temp = Label(root, text='Licht intens: {}'.format(s2.get()))
    temp.pack()


    root.mainloop()

scale = ScaleValue()
threading.Thread(target=tkinter_loop, args=(scale,)).start()

#testing a commit with this comment
while 1:
    time.sleep(1)
    print(scale.value1, scale.value2)

from tkinter import TOP, LabelFrame, Tk, Label, Button, Entry, Frame, Toplevel, ttk, PhotoImage, messagebox
from turtle import title
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)
reader = SimpleMFRC522()

def Validar_tarjeta():
    #comprobador por terminal sobre la lectura

    print ("Escaneando tarjeta")
    id, text = reader.read()
    print("ID: %s\nText: %s" % (id,text))

    if id == 385898029682:
        VentanaAdmin()
    else:
        messagebox.showwarning("Lectura incorrecta",'Esta tarjeta no esta registrada en este sistema')

def VentanaAdmin():
    VentAnd=Toplevel(VentanaPrincipal)
    VentAnd.title('Smart-tacker')
    VentAnd.attributes("-fullscreen", True)
    VentAnd.config(bg='blue') 

    FrameBajo = LabelFrame(VentAnd)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=520)


    img = ImageTk.PhotoImage(file='LogoItb.png')  
    Ibuto = Button(FrameBajo, text = 'Click Me !', image = img,width=40, height=55)
    Ibuto.place(y=100, x=990)


    #https://recursospython.com/guias-y-manuales/boton-button-en-tkinter/
    boton1 = Button (VentAnd,text='prueba',width=25, height=15)
    boton1.place(x=100, y=650)


    boton2 = Button (VentAnd, text='Prueba2',width=25, height=15)
    boton2.place(x=845, y=650)


    boton3 = Button (VentAnd, text='Prueba2',width=25, height=15, command=VentanaPrincipal.destroy)
    boton3.place(x=1590, y=650)































VentanaPrincipal = Tk() 
VentanaPrincipal.title('MiniSmart')

VentanaPrincipal.attributes("-fullscreen", True)

Frame1 = LabelFrame (VentanaPrincipal, bg='red')
Frame1.pack (side='left')
Frame1.config(width="1100", height="1920")
boton = Frame (Frame1,bg='red')
Button (text='aque', fg='red',command=Validar_tarjeta).pack(side='top')


#Frame 2
Frame2 = LabelFrame (VentanaPrincipal, bg='aqua')
Frame2.pack()
Frame2.config(width="1000", height="1920")
Frame2.config (cursor="spider")
Button (Frame2,text='aqui', fg='red',command=VentanaPrincipal.destroy).pack(side='top', expand=True)




VentanaPrincipal.mainloop()
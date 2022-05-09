from tkinter import TOP, LabelFrame, Tk, Label, Button, Entry, Frame, Toplevel, ttk, PhotoImage, messagebox
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)
reader = SimpleMFRC522()


import pymysql

#connection  = pymysql.connect(
#    host='localhost',
#    user='pi',
#    passwd='1234',
#    db="DB_layout_institutos",
#)
#print ('Conexion Establecida con la base de Datos ')


#cursor = connection.cursor()



def Validar_tarjeta():
    #comprobador por terminal sobre la lectura

    print ("Escaneando tarjeta")
    id, text = reader.read()
    print("ID: %s\nText: %s" % (id,text))

    admin='administrador'
    user = 'usuario'

    #sql = """ SELECT * FROM DB_layout_institutos"""
    #cursor.execute(sql)

    #for datos in cursor:
    #    print(datos)

    if id == 253300343202:
        VentanaAdmin(admin)
    elif id == 385898029682:
        VentanaUsuario(user)
    else:
        messagebox.showwarning("Lectura incorrecta",'Esta tarjeta no esta registrada en este sistema, ponte en contacto con un administrador')



def VentanaAdmin(usuario):
    global imagentt

    #ventana Principal
    VentAnd=Toplevel()
    VentAnd.title('Smart-tacker')
    VentAnd.attributes("-fullscreen", True)
    VentAnd.config(bg='red') #COLOR

    #frame 
    FrameBajo = LabelFrame(VentAnd)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=520,bg='#e7dbcb')

    Label(VentAnd,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=845, y=150) 
    Label(VentAnd,text=usuario,font=("Consolas", 25),bg='#e7dbcb').place(x=840,y=450)

    #boton1
    #https://recursospython.com/guias-y-manuales/boton-button-en-tkinter/

    Button (VentAnd, width=25, height=15,command=Alta).place(x=100, y=650)

    #boton2
    Button (VentAnd, text='Prueba2',width=25, height=15,command=VentAnd.destroy).place(x=845, y=650)

    #boton3
    Button (VentAnd, text='Prueba2',width=25, height=15, command=VentanaPrincipal.destroy).place(x=1590, y=650)

    #boton cerrar
    Button (VentAnd,text='X',command=VentAnd.destroy).place(x=4,y=4)
    

def imput():
    Nombre = Nombre.get()
    apellido = apellido.get()
    clase = clase.get
    tipo =  tipo.get()


def Alta():
    global img2
    #ventana Principal
    VentAlt=Toplevel()
    VentAlt.title('Smart-tacker')
    VentAlt.attributes("-fullscreen", True)
    VentAlt.config(bg='red') #COLOR

    #frame 
    FrameAlt = LabelFrame(VentAlt)
    FrameAlt.pack (side='top')
    FrameAlt.config(width=1980, height=520,bg='#e7dbcb')

    #frame2
    FrameAzul = Label(VentAlt, width=90, height=520, bg='red')
    FrameAzul.place(x=1300,y=520)


    E1 = Entry(VentAlt).place(x=100,y=700)
    E2 = Entry(VentAlt).place(x=300,y=700)
    E3 = Entry(VentAlt).place(x=600,y=700)
    E4 = Entry(VentAlt).place(x=1000,y=700)

    Button (VentAlt, text='comprobar', width=400, height=400, image=img2).place(x=1420, y=600)

    #boton cerrar
    Button (VentAlt,text='X',command=VentAlt.destroy).place(x=4,y=4)



def VentanaUsuario(usuario):
    global imagentt

    VentUsu=Toplevel(VentanaPrincipal)
    VentUsu.attributes("-fullscreen", True)
    VentUsu.config(bg='#7B1FA2') #COLOR

    FrameBajo = LabelFrame(VentUsu)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=520,bg='#e7dbcb')

    Label(VentUsu,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentUsu,text=usuario,font=("Consolas", 14)).place(x=940,y=450)

    #boton 1
    Button (VentUsu,text='prueba',width=25, height=15,command=VentUsu.destroy).place(x=540, y=650)
    
    #boton 2
    Button (VentUsu, text='Prueba2',width=25, height=15, command=VentanaPrincipal.destroy).place(x=1150, y=650)

    #boton cerrar
    Button (VentUsu,text='X',command=VentUsu.destroy).place(x=4,y=4)








VentanaPrincipal = Tk() 
VentanaPrincipal.config(bg='#e7dbcb')
VentanaPrincipal.attributes("-fullscreen", True)

#Frame azul
Frame1 = LabelFrame (VentanaPrincipal, bg='blue')
Frame1.pack (side='left')
Frame1.config(width="1100", height="1920")
boton = Frame (Frame1,bg='red')

#lado azul
#imagen con logo
imt = Image.open('/media/pi/KINGSTON/IA/image/LogoItb.png')
imtt = imt.resize((210,210))
imagentt = ImageTk.PhotoImage(imtt)
Label(Frame1,image=imagentt,width=250,height=250).place(x=420,y=150)

#texto 
Label(Frame1,text='Clicaremos el boton para interactuar con el sistema  \nAgarraremos el llavero y lo pasaremos por el lector una vez presionado el boton \nsegun nuestro permisos interactuaremos con un menu diferente ',height=10,width=80,bg='blue', font=("Consolas", 14)).place(x=100,y=450)


img = Image.open('/media/pi/KINGSTON/IA/logo.png')
imagen1 = img.resize((300, 300))
img2 = ImageTk.PhotoImage(imagen1)

Button (text='leer', fg='red',command=Validar_tarjeta, width=400, height=400,image=img2).place(x=1320, y=350)

Button (text='Cerrar', fg='red',command=VentanaPrincipal.destroy).place(x=1860, y=1000)

VentanaPrincipal.mainloop()

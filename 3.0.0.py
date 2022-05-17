from tkinter import TOP, LabelFrame, StringVar, Tk, Label, Button, Entry, Frame, Toplevel, ttk, PhotoImage, messagebox
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

GPIO.setwarnings(False)
reader = SimpleMFRC522()

import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host = 'localhost',
        port = '3306',
        user = 'root',
        password = 'Admin',
        db = 'DB_layout_institutos'
    )

    if conexion.is_connected():
        print('conexion con exito')
        infoserver = conexion.get_server_info()
        print('info del servidor,' + infoserver)


except Error as ex:
    print('error durante la conexion:', ex)



Secreto = 0
def Secret():
    global Secreto
    Secreto = Secreto +1
    print(Secreto)
    if Secreto == 10:
        VentanaSecreta()

def VentanaSecreta():
    print('entre')
    VentanaPrincipal.destroy()
    VentSecrt=Toplevel()
    VentSecrt.title('Smart-tacker')
    VentSecrt.geometry('500x500')
    VentSecrt.config(bg='blue') #COLOR
    Label(VentSecrt,text='Version 1.1.1',font=("Consolas", 20),bg='red').pack()



def Validar_tarjeta():
    #comprobador por terminal sobre la lectura
    global conexion
    cursor= conexion.cursor()

    print ("Escaneando tarjeta")
    uid, text = reader.read()

    print(uid)
    cursor.execute('SELECT usu_id FROM `Usuarios` WHERE `usu_id`='+str(uid))
    print('1')
    if cursor.fetchone():
        print('2')
        cursor.execute('SELECT `usu_tipo` FROM `Usuarios` WHERE `usu_id`='+str(uid))
        resultado = cursor.fetchone()
        H = resultado[0]
        print(H)
        cursor.execute('SELECT `usu_nombre`, `usu_apellido` FROM `Usuarios` WHERE `usu_id` ='+str(uid))
        nombreA = cursor.fetchone()
        todo = nombreA[0]
        print(todo)
        if H == 'Administrador':
            print('admin')
            VentanaAdmin()
        elif H == 'Alumno':
            print('Alumno')
            VentanaUsuario()
    else:
        messagebox.showwarning("Lectura incorrecta",'Esta tarjeta no esta registrada en este sistema, ponte en contacto con un administrador')



def VentanaAdmin():
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
    Label(VentAnd,text='usuario',font=("Consolas", 25),bg='#e7dbcb').place(x=900,y=450)

    #boton1
    #https://recursospython.com/guias-y-manuales/boton-button-en-tkinter/

    AltaPhoto = Image.open('image/giphy.gif')
    AltaPhoto1 = AltaPhoto.resize((70, 70))
    Photo2 = ImageTk.PhotoImage(AltaPhoto1)

    Label (VentAnd,text='usuario' ).place(x=200,y=0)

    Button (VentAnd,width=25, height=15,command=MenuAlta).place(x=100, y=650)

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


def MenuAlta():
    global imagentt
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

    Label(VentAlt,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentAlt,text='Usuario Alta',font=("Consolas", 17),bg='#e7dbcb').place(x=900,y=450)

    correo = StringVar()
    nombre = StringVar()
    apellido = StringVar()
    tipo = StringVar()
    clase = StringVar()



    Entry(VentAlt,textvariable=correo).place(x=100,y=700)
    Entry(VentAlt,textvariable=nombre).place(x=450,y=700)
    Entry(VentAlt,textvariable=apellido).place(x=100,y=900)
    ttk.Combobox (VentAlt,textvariable=tipo,state="readonly",values=[' ','Alumno', 'Profe', 'Administrador''']).place(x=800,y=700)
    ttk.Combobox (VentAlt,textvariable=clase,state="readonly",values=[' ', 'SMX1A', 'SMX1B', 'SMX1C', 'SMX1D', 'SMX1E', 'SMX1F', 'SMX2A', 'SMX2B', 'SMX2C', 'SMX2E', 'ASIXc1B', 'A3Dm1A', 'DAWe1A', 'DAMr1A', 'DAMi1A', 'DAMv1A', 'ASIXc2A', 'ASIXc2B', 'DAWe2A', 'DAMr2A', 'DAMi2A', 'DAMv2A', 'MMEIA', 'MMEIB', 'BATXd1A']).place(x=800,y=900)

    Label(VentAlt, width=10, height=5).place(x=150,y=600)
    Label(VentAlt, width=10, height=5).place(x=500,y=600)
    Label(VentAlt, width=10, height=5).place(x=850,y=600)
    Label(VentAlt, width=10, height=5).place(x=150,y=800)
    Label(VentAlt, width=10, height=5).place(x=500,y=800)
    Label(VentAlt, width=10, height=5).place(x=850,y=800)


    Button (VentAlt, text='comprobar', width=400, height=400, image=img2).place(x=1420, y=600)

    #boton cerrar
    Button (VentAlt,text='X',command=VentAlt.destroy).place(x=4,y=4)

def Alta():

    sql = 'INSERT IN'
    


def VentanaUsuario():
    global imagentt

    VentUsu=Toplevel(VentanaPrincipal)
    VentUsu.title('Smart-tacker')
    VentUsu.attributes("-fullscreen", True)
    VentUsu.config(bg='#7B1FA2') #COLOR

    FrameBajo = LabelFrame(VentUsu)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=520,bg='#e7dbcb')

    Label(VentUsu,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentUsu,text='usuario',font=("Consolas", 14),bg='#e7dbcb').place(x=940,y=450)

    #boton 1
    Button (VentUsu,text='prueba',width=25, height=15,command=VentUsu.destroy).place(x=540, y=650)
    
    #boton 2
    Button (VentUsu, text='Prueba2',width=25, height=15, command=VentanaPrincipal.destroy).place(x=1150, y=650)

    #boton cerrar
    Button (VentUsu,text='X',command=VentUsu.destroy).place(x=4,y=4)



VentanaPrincipal = Tk() 
VentanaPrincipal.title('Smart-tacker')
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


#boton
img = Image.open('/media/pi/KINGSTON/IA/logo.png')
imagen1 = img.resize((300, 300))
img2 = ImageTk.PhotoImage(imagen1)

Button (text='leer', fg='red',command=Validar_tarjeta, width=400, height=400,image=img2).place(x=1320, y=350)
#----------------------------------------------------------------------------------------------------------------

#imagen logo
LogoImg = Image.open('image/Logo-SMT.png')
LogoImg1 = LogoImg.resize((70,70))
LogoImg2 = ImageTk.PhotoImage(LogoImg1)

Button (Frame1,image=LogoImg2, command=Secret).place(x=0, y=1010)


Button (text='Cerrar', fg='red',command=VentanaPrincipal.destroy).place(x=1860, y=1000)

VentanaPrincipal.mainloop()

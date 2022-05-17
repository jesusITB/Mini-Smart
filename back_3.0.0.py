from tkinter import TOP, LabelFrame, StringVar, Tk, Label, Button, Entry, Frame, Toplevel, ttk, PhotoImage, messagebox
from functools import partial
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector 
from mysql.connector import Error

GPIO.setwarnings(False)
reader = SimpleMFRC522()
#https://recursospython.com/guias-y-manuales/boton-button-en-tkinter/
#https://realpython.com/python-gui-tkinter/
#https://recursospython.com/guias-y-manuales/barra-de-progreso-progressbar-tcltk-tkinter/
#https://recursospython.com/guias-y-manuales/validar-el-contenido-de-una-caja-de-texto-en-tkinter/
 



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


#Ventana secreta en un futuro sera una ventana mas util con diferentes opciones que 
#permitira manejar las Vetana sin entrar al codigo
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

##########################################################################################################

def Validar_tarjeta():
    global conexion
    cursor= conexion.cursor()

    print ("Escaneando tarjeta")
    uid, text = reader.read()

    cursor.execute('SELECT usu_id FROM `Usuarios` WHERE `usu_id`='+str(uid))
    if cursor.fetchone():
        cursor.execute('SELECT `usu_tipo` FROM `Usuarios` WHERE `usu_id`='+str(uid))
        resultado_Id_Usu = cursor.fetchone()
        Id_Usu = resultado_Id_Usu[0]
        print(Id_Usu)
        cursor.execute('SELECT `usu_nombre`, `usu_apellido` FROM `Usuarios` WHERE `usu_id` ='+str(uid))
        resultado_Nombre = cursor.fetchone()
        Nombre_Sql_Resultado = resultado_Nombre[0] , resultado_Nombre[1]
        if Id_Usu == 'Administrador':
            VentanaAdmin(Nombre_Sql_Resultado)
        elif Id_Usu == 'Alumno':
            VentanaUsuario(Nombre_Sql_Resultado)
        elif Id_Usu == 'Profe':
            VentanaProf(Nombre_Sql_Resultado)
    else:
        messagebox.showwarning("Lectura incorrecta",'Esta tarjeta no esta registrada en nuestro sistema, ponte en contacto con un administrador')

def VentanaAdmin(Nombre_Usuario):
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

    #label
    Label(VentAnd,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=845, y=150) 
    Label(VentAnd,text='Usuario',font=("Consolas", 25),bg='#e7dbcb').place(x=900,y=450)
    Label (VentAnd,text=Nombre_Usuario,font=("Consolas", 20),bg='#e7dbcb').place(x=2,y=8)

    img = PhotoImage(file='image/dejar.png')
    #boton1
    Button (VentAnd,width=25, height=15,command=partial(MenuAlta, Nombre_Usuario),border=5).place(x=100, y=650)

    #boton2
    Button (VentAnd, text='Prueba2',width=25, height=15,command=partial(MenuAltaProduct, Nombre_Usuario),border=5).place(x=845, y=650)

    #boton3
    Button (VentAnd, text='Prueba2',width=25, height=15, command=VentanaPrincipal.destroy,border=5).place(x=1590, y=650)

    #boton cerrar
    Button (VentAnd,text='X',command=VentAnd.destroy).place(x=1880,y=4)
    
def VentanaProf(Nombre_Usuario):
    global imagentt

    #ventana Principal
    VentPro=Toplevel()
    VentPro.title('Smart-tacker')
    VentPro.attributes("-fullscreen", True)
    VentPro.config(bg='green') #COLOR

    #frame 
    FrameBajo = LabelFrame(VentPro)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=520,bg='#e7dbcb')

    #label
    Label(VentPro,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=845, y=150) 
    Label(VentPro,text='Profesor',font=("Consolas", 25),bg='#e7dbcb').place(x=900,y=450)
    Label (VentPro,text=Nombre_Usuario,font=("Consolas", 20),bg='#e7dbcb').place(x=2,y=8)

    #boton1
    Button (VentPro,width=25, height=15,command=partial(MenuAltaProf, Nombre_Usuario),border=5).place(x=100, y=650)

    #boton2
    Button (VentPro, text='Prueba2',width=25, height=15,command=partial(MenuAltaProduct,Nombre_Usuario),border=5).place(x=845, y=650)

    #boton3
    Button (VentPro, text='Prueba2',width=25, height=15, command=VentanaPrincipal.destroy,border=5).place(x=1590, y=650)

    #boton cerrar
    Button (VentPro,text='X',command=VentPro.destroy).place(x=1880,y=4)

def VentanaUsuario(Nombre_Usuario):
    global imagentt
    global conexion
    cursor= conexion.cursor()


    def Prestamo():

        uid, text = reader.read()

        try:
            cursor.execute()
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
        except:
            messagebox.showinfo(message="registro exitoso")

    def Retornar():

        uid, text = reader.read()

        try:
            cursor.execute()
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
            
        except:
            messagebox.showinfo(message="registro exitoso")

    #ventana principal
    VentUsu=Toplevel()
    VentUsu.title('Smart-tacker')
    VentUsu.attributes("-fullscreen", True)
    VentUsu.config(bg='#7B1FA2') #COLOR

    #frame
    FrameBajo = LabelFrame(VentUsu)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=520,bg='#e7dbcb')

    #label
    Label(VentUsu,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentUsu,text='Alumno',font=("Consolas", 25),bg='#e7dbcb').place(x=940,y=450)
    Label (VentUsu,text=Nombre_Usuario,font=("Consolas", 20),bg='#e7dbcb').place(x=2,y=8)

    #boton 1
    Button (VentUsu,text='Prestamo',width=25, height=15,command=Prestamo,border=5).place(x=540, y=650)
    
    #boton 2
    Button (VentUsu, text='Retornar',width=25, height=15, command=Retornar,border=5).place(x=1150, y=650)

    #boton cerrar
    Button (VentUsu,text='X',command=VentUsu.destroy).place(x=1880,y=4)

def MenuAlta(Nombre_Usuario):

    def limpiar():
        correo.set('')
        nombre.set('')
        apellido.set('')
        tipo.set('')
        clase.set('')

    def alta_Usuario():
        global conexion
        cursor= conexion.cursor()

        uid, text = reader.read()
        usu_id = str(uid)
        print(usu_id)
        try:
            cursor.execute(f"INSERT INTO Usuarios (usu_correo, usu_id, usu_nombre, usu_apellido, usu_tipo, usu_clase) VALUES ('{correo.get()}','{usu_id}','{nombre.get()}','{apellido.get()}','{tipo.get()}','{clase.get()}')")
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
            limpiar()
        except:
            messagebox.showinfo(message="registro exitoso")


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

    Label (VentAlt,text=Nombre_Usuario,font=("Consolas", 20),bg='#e7dbcb').place(x=2,y=8)
    Label(VentAlt,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentAlt,text='Usuario Alta',font=("Consolas", 17),bg='#e7dbcb').place(x=900,y=450)
    
    #varibles
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

    
    #boton comprobar usuario
    Button (VentAlt, text='comprobar', width=400, height=400, image=img2, command=alta_Usuario,border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAlt,text='X',command=VentAlt.destroy).place(x=1880,y=4)



    VentAlt.mainloop()

#cambiar
def MenuAltaProduct(Nombre_Usuario):

    def limpiarProduct():
        correo.set('')
        nombre.set('')
        apellido.set('')
        tipo.set('')

    def alta_UsuarioProduct():
        global conexion
        cursor= conexion.cursor()

        uid, text = reader.read()
        usu_id = str(uid)
        print(usu_id)
        try:
            cursor.execute(f"INSERT INTO Usuarios (usu_correo, usu_id, usu_nombre, usu_apellido, usu_tipo, usu_clase) VALUES ('{correo.get()}','{usu_id}','{nombre.get()}','{apellido.get()}','{tipo.get()}')")
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
            limpiarProduct()
        except:
            messagebox.showinfo(message="registro exitoso")


    global imagentt
    global img2
    #ventana Principal
    VentAltProducct=Toplevel()
    VentAltProducct.title('Smart-tacker')
    VentAltProducct.attributes("-fullscreen", True)
    VentAltProducct.config(bg='red') #COLOR

    #frame 
    FrameAltProduct = LabelFrame(VentAltProducct)
    FrameAltProduct.pack (side='top')
    FrameAltProduct.config(width=1980, height=520,bg='#e7dbcb')

    #frame2
    FrameAzul = Label(VentAltProducct, width=90, height=520, bg='red')
    FrameAzul.place(x=1300,y=520)

    Label(VentAltProducct,text=Nombre_Usuario,font=("Consolas", 20),bg='#e7dbcb').place(x=2,y=8)
    Label(VentAltProducct,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentAltProducct,text='Producto Alta',font=("Consolas", 17),bg='#e7dbcb').place(x=900,y=450)
    
    #varibles
    correo = StringVar()
    nombre = StringVar()
    apellido = StringVar()
    tipo = StringVar()

    Entry(VentAltProducct,textvariable=correo).place(x=100,y=700)
    Entry(VentAltProducct,textvariable=nombre).place(x=450,y=700)
    Entry(VentAltProducct,textvariable=apellido).place(x=100,y=900)
    ttk.Combobox (VentAltProducct,textvariable=tipo,state="readonly",values=[' ',]).place(x=800,y=700)

    Label(VentAltProducct, width=10, height=5).place(x=150,y=600)
    Label(VentAltProducct, width=10, height=5).place(x=500,y=600)
    Label(VentAltProducct, width=10, height=5).place(x=850,y=600)
    Label(VentAltProducct, width=10, height=5).place(x=150,y=800)
    Label(VentAltProducct, width=10, height=5).place(x=500,y=800)

    
    #boton comprobar usuario
    Button (VentAltProducct, text='comprobar', width=400, height=400, image=img2, command=alta_UsuarioProduct,border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAltProducct,text='X',command=VentAltProducct.destroy).place(x=1880,y=4)



    VentAltProducct.mainloop()
#cambiar
def MenuAltaProf(Nombre_Usuario):
    global imagentt
    global img2

    #ventana Principal
    VentAlt=Toplevel()
    VentAlt.title('Smart-tacker')
    VentAlt.attributes("-fullscreen", True)
    VentAlt.config(bg='green') #COLOR

    #frame 
    FrameAlt = LabelFrame(VentAlt)
    FrameAlt.pack (side='top')
    FrameAlt.config(width=1980, height=520,bg='#e7dbcb')

    #frame2
    FrameAzul = Label(VentAlt, width=90, height=520, bg='green')
    FrameAzul.place(x=1300,y=520)

    Label (VentAlt,text=Nombre_Usuario,font=("Consolas", 20),bg='#e7dbcb').place(x=2,y=8)
    Label(VentAlt,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentAlt,text='Usuario Alta',font=("Consolas", 17),bg='#e7dbcb').place(x=900,y=450)

    #varibles
    correo =StringVar()
    nombre =StringVar()
    apellido =StringVar()
    tipo =StringVar()
    clase =StringVar()

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

    #boton comprobar usuario
    Button (VentAlt, text='comprobar', width=400, height=400, image=img2,border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAlt,text='X',command=VentAlt.destroy).place(x=1880,y=4)

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
imt = Image.open('/media/pi/KINGSTON/IA/image/LogoItb.png')
imtt = imt.resize((210,210))
imagentt = ImageTk.PhotoImage(imtt)
Label(Frame1,image=imagentt,width=250,height=250).place(x=420,y=150)

#texto 
Label(Frame1,text='Clicaremos el boton para interactuar con el sistema  \nAgarraremos el llavero y lo pasaremos por el lector una vez presionado el boton \nsegun nuestro permisos interactuaremos con un menu diferente ',height=10,width=80,bg='blue', fg='white',font=("Consolas", 14)).place(x=100,y=450)

#boton
img = Image.open('/media/pi/KINGSTON/IA/logo.png')
imagen1 = img.resize((300, 300))
img2 = ImageTk.PhotoImage(imagen1)

Button (text='leer', fg='red',command=Validar_tarjeta, width=400, height=400,image=img2,border=8).place(x=1320, y=350)
#----------------------------------------------------------------------------------------------------------------
#imagen logo
LogoImg = Image.open('image/Logo-SMT.png')
LogoImg1 = LogoImg.resize((70,70))
LogoImg2 = ImageTk.PhotoImage(LogoImg1)

#boton logo de empresa
Button (Frame1,image=LogoImg2, command=Secret).place(x=0, y=1010)

Button (text='Cerrar', fg='red',command=VentanaPrincipal.destroy).place(x=1860, y=1000)

VentanaPrincipal.mainloop()

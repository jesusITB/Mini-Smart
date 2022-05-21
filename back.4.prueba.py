from tkinter import CENTER, TOP, LabelFrame, StringVar, Tk, Label, Button, Entry, Frame, Toplevel, ttk, PhotoImage, messagebox
from functools import partial
from PIL import ImageTk, Image
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector 
from mysql.connector import Error
from datetime import datetime

date = datetime.now()
GPIO.setwarnings(False)
reader = SimpleMFRC522()
#https://recursospython.com/guias-y-manuales/boton-button-en-tkinter/
#https://realpython.com/python-gui-tkinter/
#https://recursospython.com/guias-y-manuales/barra-de-progreso-progressbar-tcltk-tkinter/
#https://recursospython.com/guias-y-manuales/validar-el-contenido-de-una-caja-de-texto-en-tkinter/

#https://pimylifeup.com/raspberry-pi-rfid-rc522/




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
    cursor= conexion.cursor()

    print ("Escaneando tarjeta")
    uid, text = reader.read()

    id_usuario_global = uid
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
            VentanaAdmin(Nombre_Sql_Resultado,conexion)
        elif Id_Usu == 'Alumno':
            VentanaUsuario(Nombre_Sql_Resultado,id_usuario_global,conexion)
        elif Id_Usu == 'Profe':
            VentanaProf(Nombre_Sql_Resultado,conexion)
    else:
        messagebox.showwarning("Lectura incorrecta",'Esta tarjeta no esta registrada en nuestro sistema, ponte en contacto con un administrador')

##########################################################################################################

def VentanaAdmin(Nombre_Usuario,conexion):
    global imagentt

    #ventana Principal
    VentAnd=Toplevel()
    VentAnd.title('Smart-tacker')
    VentAnd.attributes("-fullscreen", True)
    VentAnd.config(bg='red') #COLOR

    #frame 
    FrameBajo = LabelFrame(VentAnd)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=480,bg='#e7dbcb')

    #label
    Label(VentAnd,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=835, y=150) 
    Label(VentAnd,text='Administrador',font=("Consolas", 21),bg='#e7dbcb').place(x=850,y=400)
    Label (VentAnd,text=Nombre_Usuario,font=("Consolas", 20),bg='red',fg='white').pack()

    
    #boton1
    imgB1 = PhotoImage(file='image/Alta_Usuario.png')
    Button (VentAnd,width=250, height=250,command=partial(MenuAlta, Nombre_Usuario,conexion),border=5,image=imgB1).place(x=100, y=650)
    Label(VentAnd,text='Alta Usuario',border=5).place(x=190,y=600)

    #boton2
    imgB2 = PhotoImage(file='image/Producto.png')
    Button (VentAnd, text='Prueba2',width=250, height=250,command=partial(MenuAltaProduct, Nombre_Usuario,conexion),border=5,image=imgB2).place(x=830, y=650)
    Label(VentAnd,text='Alta Producto',border=5).place(x=910,y=600)

    #boton3
    imgB3 = PhotoImage(file='image/Lista.png')
    Button (VentAnd, text='Prueba2',width=250, height=250, command=partial(MenuListaDB, Nombre_Usuario,conexion),border=5,image=imgB3).place(x=1590, y=650)
    Label(VentAnd,text='Lista Usuario',border=5).place(x=1680,y=600)

    #boton cerrar
    Button (VentAnd,text='X',command=VentAnd.destroy,width=3, height=2).place(x=1860,y=4)

    VentAnd.mainloop()

def MenuAlta(Nombre_Usuario,conexion):

    def limpiar():
        correo.set('')
        nombre.set('')
        apellido.set('')
        tipo.set('')
        clase.set('')

    def alta_Usuario(conexion):
        cursor= conexion.cursor()

        uid, text = reader.read()
        usu_id = int(uid)
        print(clase.get())

        try:
            cursor.execute(f"INSERT INTO Usuarios (usu_correo, usu_id, usu_nombre, usu_apellido, usu_tipo, usu_clase) VALUES('{correo.get()}', '{usu_id}', '{nombre.get()}', '{apellido.get()}', '{tipo.get()}', '{clase.get()}');")
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
            limpiar()
        except Error as ex:
            print('error durante la conexion:', ex)
            messagebox.showinfo(message="registro fallido")


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
    FrameAlt.config(width=1980, height=480,bg='#e7dbcb')

    Label (VentAlt,text=Nombre_Usuario,font=("Consolas", 20),bg='red',fg='white').pack()
    Label(VentAlt,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=835, y=150) 
    Label(VentAlt,text='Usuario Alta',font=("Consolas", 21),bg='#e7dbcb').place(x=850,y=400)

    
    #varibles
    correo = StringVar()
    nombre = StringVar()
    apellido = StringVar()
    tipo = StringVar()
    clase = StringVar()

    ImgNombre = PhotoImage(file='image/nombre.png')
    Label(VentAlt,image=ImgNombre,bg='red').place(x=110,y=610)
    Label(VentAlt,text='nombre').place(x=150,y=580)
    Entry(VentAlt,textvariable=nombre).place(x=80,y=750)

    ImgApellido = PhotoImage(file='image/apellido.png')
    Label(VentAlt,image=ImgApellido,bg='red').place(x=460,y=610)
    Label(VentAlt,text='apellido').place(x=500,y=580)
    Entry(VentAlt,textvariable=apellido).place(x=450,y=750)

    ImgCorreo = PhotoImage(file='image/correo.png')
    Label(VentAlt,image=ImgCorreo,bg='red').place(x=800,y=610)
    Label(VentAlt,text='correo').place(x=850,y=580)
    Entry(VentAlt,textvariable=correo).place(x=785,y=750)
###########################################

    Imgtipo = PhotoImage(file='image/tipo.png')
    Label(VentAlt,image=Imgtipo,bg='red').place(x=100,y=850)
    Label(VentAlt,text='tipo').place(x=150,y=800)
    ttk.Combobox (VentAlt,textvariable=tipo,state="readonly",values=[' ','Alumno', 'Profe', 'Administrador''']).place(x=80,y=1000)

    ImgClase = PhotoImage(file='image/clase.png')
    Label(VentAlt,image=ImgClase,bg='red').place(x=450,y=850)
    Label(VentAlt,text='clase').place(x=500,y=800)
    ttk.Combobox (
        VentAlt,
        textvariable=clase,
        state="readonly",
        values=['PROFESSOR', 'SMX1A', 'SMX1B', 'SMX1C', 'SMX1D', 'SMX1E', 'SMX1F', 'SMX2A', 'SMX2B', 'SMX2C', 'SMX2E', 'ASIXc1B', 'A3Dm1A', 'DAWe1A', 'DAMr1A', 'DAMi1A', 'DAMv1A', 'ASIXc2A', 'ASIXc2B', 'DAWe2A', 'DAMr2A', 'DAMi2A', 'DAMv2A', 'MMEIA', 'MMEIB', 'BATXd1A']
        ).place(x=430,y=1000)
    #boton comprobar usuario
    Button (VentAlt, text='comprobar', width=400, height=400, image=img2, command=partial(alta_Usuario,conexion),border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAlt,text='X',command=VentAlt.destroy,width=3, height=2).place(x=1860,y=4)



    VentAlt.mainloop()

def MenuAltaProduct(Nombre_Usuario,conexion):

    def alta_UsuarioProduct(conexion):
        cursor= conexion.cursor()

        uid, text = reader.read()
        pro_id = int(uid) 
        precio_A = int(precio.get())                                                                                                                                       
        try:
            cursor.execute(f"INSERT INTO `Producto` (`pro_id`, `pro_nombre`, `pro_descripcion`, `pro_familia`, `pro_estado`, `pro_fecha_compra`, `pro_precio`, `pro_solicitante_compra`,`pro_disponibilidad`)VALUES({pro_id}, '{nombre.get()}', '{Descripcion.get()}', '{tipo.get()}', '{estado.get()}', '2022-05-10', '{precio_A}', '{solicitante.get()}','Disponible');")
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
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
    FrameAltProduct.config(width=1980, height=480,bg='#e7dbcb')

    Label (VentAltProducct,text=Nombre_Usuario,font=("Consolas", 20),bg='red',fg='white').pack()
    Label(VentAltProducct,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=835, y=150) 
    Label(VentAltProducct,text='Producto Alta',font=("Consolas", 21),bg='#e7dbcb').place(x=850,y=400)
    
    #varibles
    estado = StringVar()
    nombre = StringVar()
    precio = StringVar()
    tipo = StringVar()
    Descripcion = StringVar()
    solicitante = StringVar()

    ImgNombre = PhotoImage(file='image/nombre.png')
    Label(VentAltProducct,image=ImgNombre,bg='red').place(x=110,y=610)
    Label(VentAltProducct,text='Nombre').place(x=150,y=580)
    Entry(VentAltProducct,textvariable=nombre).place(x=100,y=750)

    ImgEstado = PhotoImage(file='image/estado.png')
    Label(VentAltProducct,image=ImgEstado,bg='red').place(x=450,y=610)
    Label(VentAltProducct,text='Estado').place(x=490,y=580)
    ttk.Combobox(VentAltProducct,textvariable=estado,values=['','EN PERFECTO ESTADO','EN BUEN ESTADO','EN ESTADO NORMAL','EN MAL ESTADO' ,]).place(x=420,y=750)

##########################################################################
    ImgPrecio = PhotoImage(file='image/precio.png')
    Label(VentAltProducct,image=ImgPrecio,bg='red').place(x=110,y=850)
    Label(VentAltProducct,text='precio').place(x=150,y=800)
    Entry(VentAltProducct,textvariable=precio).place(x=90,y=1000)
    
    ImgSolicitante = PhotoImage(file='image/solicitante.png')
    Label(VentAltProducct,image=ImgSolicitante,bg='red').place(x=440,y=850)
    Label (VentAltProducct,text='Solicitante').place(x=470,y=800)
    Entry(VentAltProducct,textvariable=solicitante).place(x=420,y=1000)

    ImgTipo = PhotoImage(file='image/tipo_Producto.png')
    Label(VentAltProducct,image=ImgTipo,bg='red').place(x=770,y=850)
    Label(VentAltProducct,text='tipo').place(x=810,y=800)
    ttk.Combobox (
        VentAltProducct,
        textvariable=tipo,
        state="readonly",
        values=['','Protector silicona','Estoig viatge','Ulleres VR Oculus Quest 2',
    'Comandaments consola','Webcam','Drons','Protector drons','Bateria drons','Tornavisos','Escanner de Barres','Adaptador USB-C','Gimbal',
    'Ulleres VR Pico Neo 3 pro','Ulleres VR- HP rever g2','Ulleres VR Microsoft Hololens','Pinça Onrobot Gripper', 'Raspberry pi 4','Raspberry pi 4',
    'Raspberry Pi 4 b 4Gb car','Raspberry Pi 4 b 4Gb','Rasperrry Pi 3 A','Raspberry pi 4',
    'Modulo GPS','Raspberry pi 4','Raspberry pi 4','Raspberry pi 4','Tauleta Wacom''Raspberry pi 4','Raspberry pi 4','Elego Starter Kit de Arduino',
    'arduino car','Raspberry pi 4','Raspberry pi 4','Raspberry pi 4','sensor infraroig','carcasa i rodes cotxe',
    'clauers RFID','GPS','WIFI ','sensor luz ',]
    ).place(x=750,y=1000)

##################################################
    Label (VentAltProducct,text='descripcion').place(x=1130,y=650)
    Entry(VentAltProducct,textvariable=Descripcion).place(x=1000,y=700,width=350,height=250)

    #boton comprobar usuario
    Button (VentAltProducct, text='comprobar', width=400, height=400, image=img2, command=partial(alta_UsuarioProduct,conexion),border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAltProducct,text='X',command=VentAltProducct.destroy,width=3, height=2).place(x=1860,y=4)



    VentAltProducct.mainloop()

def MenuListaDB(Nombre_Usuario,conexion):
    cursor= conexion.cursor()


    def Eliminar():
        correo = lista.selection()[0]
        cursor.execute(f"DELETE FROM `Usuarios` WHERE `Usuarios`.`usu_correo` ='{correo}'")
        conexion.commit()
        lista.delete(correo)


    imgL = Image.open('image/LogoItb.png')
    imgLl = imgL.resize((150,150))
    imagenMini = ImageTk.PhotoImage(imgLl)


    #ventana Principal
    VentList=Toplevel()
    VentList.title('Smart-tacker')
    VentList.attributes("-fullscreen", True)
    VentList.config(bg='red') #COLOR

    #frame 
    FrameAlt = LabelFrame(VentList)
    FrameAlt.pack (side='top')
    FrameAlt.config(width=1980, height=300,bg='#e7dbcb')

    #frame2
    FrameAzul = Label(VentList, width=40, height=100, bg='blue')
    FrameAzul.place(x=0,y=0)

    Label(VentList,text=Nombre_Usuario,font=("Consolas", 20),bg='red',fg='white').place(x=1040,y=300)
    Label(VentList,image=imagenMini,width=200,height=200,bg='#e7dbcb').place(x=1050,y=50) 
    Label(VentList,text='Lista',font=("Consolas", 17),bg='#e7dbcb').place(x=1115,y=250)

    lista = ttk.Treeview(VentList)
    lista.place(x=400,y=400)
    lista['columns']=('correo','id','Nombre','apellido','tipo','clase',)
    lista.column('#0', width=0,stretch='NO')
    lista.column('correo',anchor=CENTER)
    lista.column('id',anchor=CENTER)
    lista.column('Nombre',anchor=CENTER)
    lista.column('apellido',anchor=CENTER)
    lista.column('tipo',anchor=CENTER)
    lista.column('clase',anchor=CENTER)
    lista.heading('#0',text="",anchor=CENTER)
    lista.heading('correo',text="correo",anchor=CENTER)
    lista.heading('id',text="id",anchor=CENTER)
    lista.heading('Nombre',text="Nombre",anchor=CENTER)
    lista.heading('apellido',text="apellido",anchor=CENTER)
    lista.heading('tipo',text="tipo",anchor=CENTER)
    lista.heading('clase',text="clase",anchor=CENTER)


    def VaciaTabla():
        filas=lista.get_children()
        for fila in filas:
            lista.delete(fila)

    def llenarTabla():
        VaciaTabla()
        sql = "SELECT * FROM `Usuarios` ORDER BY `Usuarios`.`usu_tipo` ASC"
        cursor.execute(sql)
        filas = cursor.fetchall()
        for fila in filas:
            correo = fila[0]
            lista.insert('','end', correo, text= correo, values=fila)

    llenarTabla()


    Label(FrameAzul, text='OPCIONES',font=("Consolas", 39),bg='blue',fg='white').place(x=4,y=4)
    #boton
    Button(FrameAzul, text='Eliminar', command=lambda:Eliminar()).place(x=20,y=100,width=190)

    #boton
    Button(FrameAzul, text='vaciar', command=lambda:VaciaTabla()).place(x=20,y=150,width=190)




    #boton cerrar
    Button (VentList,text='X',command=VentList.destroy,width=3, height=2).place(x=1860,y=4)

    VentList.mainloop()

##########################################################################################################

def VentanaProf(Nombre_Usuario,conexion):
    global imagentt

    #ventana Principal
    VentPro=Toplevel()
    VentPro.title('Smart-tacker')
    VentPro.attributes("-fullscreen", True)
    VentPro.config(bg='green') #COLOR

    #frame 
    FrameBajo = LabelFrame(VentPro)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=480,bg='#e7dbcb')

    #label
    Label(VentPro,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=835, y=150) 
    Label(VentPro,text='Administrador',font=("Consolas", 21),bg='#e7dbcb').place(x=850,y=400)
    Label (VentPro,text=Nombre_Usuario,font=("Consolas", 20),bg='green',fg='white').pack()

    
    #boton1
    imgB1 = PhotoImage(file='image/Alta_Usuario.png')
    Button (VentPro,width=250, height=250,command=partial(MenuAltaProf, Nombre_Usuario,conexion),border=5,image=imgB1).place(x=100, y=650)
    Label(VentPro,text='Alta Usuario',border=5).place(x=190,y=600)

    #boton2
    imgB2 = PhotoImage(file='image/Producto.png')
    Button (VentPro, text='Prueba2',width=250, height=250,command=partial(MenuAltaProduct, Nombre_Usuario,conexion),border=5,image=imgB2).place(x=830, y=650)
    Label(VentPro,text='Alta Producto',border=5).place(x=910,y=600)

    #boton3
    imgB3 = PhotoImage(file='image/Lista.png')
    Button (VentPro, text='Prueba2',width=250, height=250, command=partial(MenuListaDB_profe, Nombre_Usuario,conexion),border=5,image=imgB3).place(x=1590, y=650)
    Label(VentPro,text='Lista Usuario',border=5).place(x=1680,y=600)

    #boton cerrar
    Button (VentPro,text='X',command=VentPro.destroy,width=3, height=2).place(x=1860,y=4)
    
    VentPro.mainloop()
#cambiar
def MenuAltaProf(Nombre_Usuario,conexion):
    global imagentt
    global img2

    def limpiar():
        correo.set('')
        nombre.set('')
        apellido.set('')
        tipo.set('')
        clase.set('')

    def alta_Usuario(conexion):
        cursor= conexion.cursor()

        uid, text = reader.read()
        usu_id = int(uid)
        print(clase.get())

        try:
            cursor.execute(f"INSERT INTO Usuarios (usu_correo, usu_id, usu_nombre, usu_apellido, usu_tipo, usu_clase) VALUES('{correo.get()}', '{usu_id}', '{nombre.get()}', '{apellido.get()}', '{tipo.get()}', '{clase.get()}');")
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
            limpiar()
        except Error as ex:
            print('error durante la conexion:', ex)
            messagebox.showinfo(message="registro fallido")


    #ventana Principal
    VentAltP=Toplevel()
    VentAltP.title('Smart-tacker')
    VentAltP.attributes("-fullscreen", True)
    VentAltP.config(bg='green') #COLOR

    #frame 
    FrameAlt = LabelFrame(VentAltP)
    FrameAlt.pack (side='top')
    FrameAlt.config(width=1980, height=480,bg='#e7dbcb')

    Label (VentAltP,text=Nombre_Usuario,font=("Consolas", 20),bg='green',fg='white').pack()
    Label(VentAltP,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=835, y=150) 
    Label(VentAltP,text='Usuario Alta',font=("Consolas", 21),bg='#e7dbcb').place(x=850,y=400)

    
    #varibles
    correo = StringVar()
    nombre = StringVar()
    apellido = StringVar()
    tipo = StringVar()
    clase = StringVar()

    ImgNombre = PhotoImage(file='image/nombre.png')
    Label(VentAltP,image=ImgNombre,bg='green').place(x=110,y=610)
    Label(VentAltP,text='nombre').place(x=150,y=580)
    Entry(VentAltP,textvariable=nombre).place(x=100,y=750)

    ImgApellido = PhotoImage(file='image/apellido.png')
    Label(VentAltP,image=ImgApellido,bg='green').place(x=460,y=610)
    Label(VentAltP,text='apellido').place(x=500,y=580)
    Entry(VentAltP,textvariable=apellido).place(x=450,y=750)

    ImgCorreo = PhotoImage(file='image/correo.png')
    Label(VentAltP,image=ImgCorreo,bg='green').place(x=800,y=610)
    Label(VentAltP,text='correo').place(x=850,y=580)
    Entry(VentAltP,textvariable=correo).place(x=785,y=750)
###########################################

    Imgtipo = PhotoImage(file='image/tipo.png')
    Label(VentAltP,image=Imgtipo,bg='green').place(x=100,y=850)
    Label(VentAltP,text='tipo').place(x=150,y=800)
    ttk.Combobox (VentAltP,textvariable=tipo,state="readonly",values=[' ','Alumno', 'Profe', 'Administrador''']).place(x=80,y=1000)

    ImgClase = PhotoImage(file='image/clase.png')
    Label(VentAltP,image=ImgClase,bg='green').place(x=450,y=850)
    Label(VentAltP,text='clase').place(x=500,y=800)
    ttk.Combobox (
        VentAltP,
        textvariable=clase,
        state="readonly",
        values=['PROFESSOR', 'SMX1A', 'SMX1B', 'SMX1C', 'SMX1D', 'SMX1E', 'SMX1F', 'SMX2A', 'SMX2B', 'SMX2C', 'SMX2E', 'ASIXc1B', 'A3Dm1A', 'DAWe1A', 'DAMr1A', 'DAMi1A', 'DAMv1A', 'ASIXc2A', 'ASIXc2B', 'DAWe2A', 'DAMr2A', 'DAMi2A', 'DAMv2A', 'MMEIA', 'MMEIB', 'BATXd1A']
        ).place(x=430,y=1000)
    #boton comprobar usuario
    Button (VentAltP, text='comprobar', width=400, height=400, image=img2, command=partial(alta_Usuario,conexion),border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAltP,text='X',command=VentAltP.destroy,width=3, height=2).place(x=1860,y=4)

    VentAltP.mainloop()

def MenuAltaProduct(Nombre_Usuario,conexion):
    cursor= conexion.cursor()

    def alta_UsuarioProduct(conexion):
        cursor= conexion.cursor()

        uid, text = reader.read()
        pro_id = int(uid) 
        precio_A = int(precio.get())                                                                                                                                       
        try:
            cursor.execute(f"INSERT INTO `Producto` (`pro_id`, `pro_nombre`, `pro_descripcion`, `pro_familia`, `pro_estado`, `pro_fecha_compra`, `pro_precio`, `pro_solicitante_compra`,`pro_disponibilidad`)VALUES({pro_id}, '{nombre.get()}', '{Descripcion.get()}', '{tipo.get()}', '{estado.get()}', '2022-05-10', '{precio_A}', '{solicitante.get()}','Disponible');")
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
        except:
            messagebox.showinfo(message="registro exitoso")


    global imagentt
    global img2
    #ventana Principal
    VentAltProducct_P=Toplevel()
    VentAltProducct_P.title('Smart-tacker')
    VentAltProducct_P.attributes("-fullscreen", True)
    VentAltProducct_P.config(bg='green') #COLOR

    #frame 
    FrameAltProduct = LabelFrame(VentAltProducct_P)
    FrameAltProduct.pack (side='top')
    FrameAltProduct.config(width=1980, height=480,bg='#e7dbcb')

    Label (VentAltProducct_P,text=Nombre_Usuario,font=("Consolas", 20),bg='green',fg='white').pack()
    Label(VentAltProducct_P,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=835, y=150) 
    Label(VentAltProducct_P,text='Producto Alta',font=("Consolas", 21),bg='#e7dbcb').place(x=850,y=400)
    
    #varibles
    estado = StringVar()
    nombre = StringVar()
    precio = StringVar()
    tipo = StringVar()
    Descripcion = StringVar()
    solicitante = StringVar()

    ImgNombre = PhotoImage(file='image/nombre.png')
    Label(VentAltProducct_P,image=ImgNombre,bg='green').place(x=110,y=610)
    Label(VentAltProducct_P,text='Nombre').place(x=150,y=580)
    Entry(VentAltProducct_P,textvariable=nombre).place(x=100,y=750)

    ImgEstado = PhotoImage(file='image/estado.png')
    Label(VentAltProducct_P,image=ImgEstado,bg='green').place(x=450,y=610)
    Label(VentAltProducct_P,text='Estado').place(x=490,y=580)
    ttk.Combobox(VentAltProducct_P,textvariable=estado,values=['','EN PERFECTO ESTADO','EN BUEN ESTADO','EN ESTADO NORMAL','EN MAL ESTADO' ,]).place(x=420,y=750)

##########################################################################
    ImgPrecio = PhotoImage(file='image/precio.png')
    Label(VentAltProducct_P,image=ImgPrecio,bg='green').place(x=110,y=850)
    Label(VentAltProducct_P,text='precio').place(x=150,y=800)
    Entry(VentAltProducct_P,textvariable=precio).place(x=90,y=1000)
    
    ImgSolicitante = PhotoImage(file='image/solicitante.png')
    Label(VentAltProducct_P,image=ImgSolicitante,bg='green').place(x=440,y=850)
    Label (VentAltProducct_P,text='Solicitante').place(x=470,y=800)
    Entry(VentAltProducct_P,textvariable=solicitante).place(x=420,y=1000)

    ImgTipo = PhotoImage(file='image/tipo_Producto.png')
    Label(VentAltProducct_P,image=ImgTipo,bg='green').place(x=770,y=850)
    Label(VentAltProducct_P,text='tipo').place(x=810,y=800)
    ttk.Combobox (
        VentAltProducct_P,
        textvariable=tipo,
        state="readonly",
        values=['','Protector silicona','Estoig viatge','Ulleres VR Oculus Quest 2',
    'Comandaments consola','Webcam','Drons','Protector drons','Bateria drons','Tornavisos','Escanner de Barres','Adaptador USB-C','Gimbal',
    'Ulleres VR Pico Neo 3 pro','Ulleres VR- HP rever g2','Ulleres VR Microsoft Hololens','Pinça Onrobot Gripper', 'Raspberry pi 4','Raspberry pi 4',
    'Raspberry Pi 4 b 4Gb car','Raspberry Pi 4 b 4Gb','Rasperrry Pi 3 A','Raspberry pi 4',
    'Modulo GPS','Raspberry pi 4','Raspberry pi 4','Raspberry pi 4','Tauleta Wacom''Raspberry pi 4','Raspberry pi 4','Elego Starter Kit de Arduino',
    'arduino car','Raspberry pi 4','Raspberry pi 4','Raspberry pi 4','sensor infraroig','carcasa i rodes cotxe',
    'clauers RFID','GPS','WIFI ','sensor luz ',]
    ).place(x=750,y=1000)

##################################################
    Label (VentAltProducct_P,text='descripcion').place(x=1130,y=650)
    Entry(VentAltProducct_P,textvariable=Descripcion).place(x=1000,y=700,width=350,height=250)

    #boton comprobar usuario
    Button (VentAltProducct_P, text='comprobar', width=400, height=400, image=img2, command=partial(alta_UsuarioProduct,conexion),border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAltProducct_P,text='X',command=VentAltProducct_P.destroy,width=3, height=2).place(x=1860,y=4)

    VentAltProducct_P.mainloop()
#cambiar
def MenuListaDB_profe(Nombre_Usuario,conexion):
    cursor= conexion.cursor()


    def Eliminar():
        correo = lista.selection()[0]
        cursor.execute(f"DELETE FROM `Usuarios` WHERE `Usuarios`.`usu_correo` ='{correo}'")
        conexion.commit()
        lista.delete(correo)


    imgL = Image.open('image/LogoItb.png')
    imgLl = imgL.resize((150,150))
    imagenMini = ImageTk.PhotoImage(imgLl)


    #ventana Principal
    VentListP=Toplevel()
    VentListP.title('Smart-tacker')
    VentListP.attributes("-fullscreen", True)
    VentListP.config(bg='green') #COLOR

    #frame 
    FrameAlt = LabelFrame(VentListP)
    FrameAlt.pack (side='top')
    FrameAlt.config(width=1980, height=300,bg='#e7dbcb')

    #frame2
    FrameAzul = Label(VentListP, width=40, height=100, bg='blue')
    FrameAzul.place(x=0,y=0)

    Label(VentListP,text=Nombre_Usuario,font=("Consolas", 20),bg='green',fg='white').place(x=1040,y=300)
    Label(VentListP,image=imagenMini,width=200,height=200,bg='#e7dbcb').place(x=1050,y=50) 
    Label(VentListP,text='Lista',font=("Consolas", 17),bg='#e7dbcb').place(x=1115,y=250)

    lista = ttk.Treeview(VentListP)
    lista.place(x=400,y=400)
    lista['columns']=('correo','id','Nombre','apellido','tipo','clase',)
    lista.column('#0', width=0,stretch='NO')
    lista.column('correo',anchor=CENTER)
    lista.column('id',anchor=CENTER)
    lista.column('Nombre',anchor=CENTER)
    lista.column('apellido',anchor=CENTER)
    lista.column('tipo',anchor=CENTER)
    lista.column('clase',anchor=CENTER)
    lista.heading('#0',text="",anchor=CENTER)
    lista.heading('correo',text="correo",anchor=CENTER)
    lista.heading('id',text="id",anchor=CENTER)
    lista.heading('Nombre',text="Nombre",anchor=CENTER)
    lista.heading('apellido',text="apellido",anchor=CENTER)
    lista.heading('tipo',text="tipo",anchor=CENTER)
    lista.heading('clase',text="clase",anchor=CENTER)


    def VaciaTabla():
        filas=lista.get_children()
        for fila in filas:
            lista.delete(fila)

    def llenarTabla():
        VaciaTabla()
        sql = "SELECT * FROM `Usuarios` ORDER BY `Usuarios`.`usu_tipo` ASC"
        cursor.execute(sql)
        filas = cursor.fetchall()
        for fila in filas:
            correo = fila[0]
            lista.insert('','end', correo, text= correo, values=fila)

    llenarTabla()


    Label(FrameAzul, text='OPCIONES',font=("Consolas", 39),bg='blue',fg='white').place(x=4,y=4)
    #boton
    Button(FrameAzul, text='Eliminar', command=lambda:Eliminar()).place(x=20,y=100,width=190)

    #boton
    Button(FrameAzul, text='vaciar', command=lambda:VaciaTabla()).place(x=20,y=150,width=190)




    #boton cerrar
    Button (VentListP,text='X',command=VentListP.destroy,width=3, height=2).place(x=1860,y=4)

    VentListP.mainloop()

#########################################################################################################

def VentanaUsuario(Nombre_Usuario,id_usuario_global,conexion):
    global imagentt
    cursor= conexion.cursor()


    def Prestamo():

        PresUid, text = reader.read()
        print(id_usuario_global)

        cursor.execute(f"SELECT `usu_correo` FROM `Usuarios` WHERE `usu_id`={id_usuario_global}")
        correo_usu = cursor.fetchone()
        print(f'correo={correo_usu[0]}')

        print(PresUid)

        fecha = (date.date())
        print(fecha)
        try:
            cursor.execute(f"INSERT INTO `Prestamo` (`usu_correo`, `pro_id`, `pre_fecha_prestamo`) VALUES ('{correo_usu[0]}', '{PresUid}', '{fecha}');")
            conexion.commit()
            cursor.execute(f"UPDATE `Producto` SET `pro_disponibilidad` = 'No disponible' WHERE `Producto`.`pro_id` ={PresUid};")
            conexion.commit()
            messagebox.showinfo(message="registro exitoso")
        except Error as ex:
            print('error durante la conexion:', ex)
            messagebox.showinfo(message="registro Fallido")

    def Retornar():
        RetorUid  , text = reader.read()

        fecha_R= (date.date())
        #Ventana_float()
        try:
            cursor.execute(f"UPDATE `Prestamo` SET `pre_fecha_devolucion`='{fecha_R}', `pre_activo`='No activo' WHERE `pro_id`='{RetorUid}' AND `pre_activo`='Activo';")
            conexion.commit()

            cursor.execute(f"UPDATE Producto SET pro_disponibilidad='Disponible' WHERE pro_id='{RetorUid}';")
            
            conexion.commit()
            messagebox.showinfo(message="Devolucion Exitosa")
        except Error as ex:
            messagebox.showinfo(message="Devolucion Fallido")

    #ventana principal
    VentUsu=Toplevel()
    VentUsu.title('Smart-tacker')
    VentUsu.attributes("-fullscreen", True)
    VentUsu.config(bg='#7B1FA2') #COLOR

    #frame
    FrameBajo = LabelFrame(VentUsu)
    FrameBajo.pack (side='top')
    FrameBajo.config(width=1980, height=480,bg='#e7dbcb')

    #label
    Label(VentUsu,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=830,y=150) 
    Label(VentUsu,text='Alumno',font=("Consolas", 25),bg='#e7dbcb').place(x=900,y=400)
    Label (VentUsu,text=Nombre_Usuario,font=("Consolas", 25),bg='#7B1FA2',fg='white').pack()

    #boton 1
    imgPre = PhotoImage(file='image/recoger.png',)
    Button (VentUsu,text='Prestamo',width=250, height=250,command=Prestamo,border=8, image=imgPre).place(x=510, y=650)
    Label(VentUsu,text='Prestamo',border=5).place(x=600,y=600)
    
    #boton 2
    imgRet = PhotoImage(file='image/dejar.png',)
    Button (VentUsu, text='Retornar',width=250, height=250, command=Retornar,border=8,image=imgRet).place(x=1150, y=650)
    Label(VentUsu,text='Retornar',border=5).place(x=1250,y=600)

    #boton cerrar
    Button (VentUsu,text='X',command=VentUsu.destroy,width=3, height=2).place(x=1860,y=4)
    VentUsu.mainloop()

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
imt = Image.open('image/LogoItb.png')
imtt = imt.resize((210,210))
imagentt = ImageTk.PhotoImage(imtt)
Label(Frame1,image=imagentt,width=250,height=250,bg='white').place(x=440,y=150)

#texto 
Label(Frame1,text='Clicaremos el boton para interactuar con el sistema  \nAgarraremos el llavero y lo pasaremos por el lector una vez presionado el boton \nsegun nuestro permisos interactuaremos con un menu diferente ',height=10,width=80,bg='blue', fg='white',font=("Consolas", 14)).place(x=100,y=450)

#boton
img = Image.open('image/logo.png')
imagen1 = img.resize((300, 300))
img2 = ImageTk.PhotoImage(imagen1)

Button (text='leer', fg='red',command=Validar_tarjeta, width=400, height=400,image=img2,border=8).place(x=1320, y=350)
#----------------------------------------------------------------------------------------------------------------
#imagen logo
LogoImg = Image.open('image/Logo-SMT.png')
LogoImg1 = LogoImg.resize((70,70))
LogoImg2 = ImageTk.PhotoImage(LogoImg1)

#boton logo de empresa
Button (Frame1,image=LogoImg2, command=Secret).place(x=510, y=900)
Label (Frame1,text='Smart Tracker',font=("Consolas", 14),bg='blue').place(x=470,y=1000)

Button (text='Cerrar', fg='red',command=VentanaPrincipal.destroy).place(x=1860, y=1000)


VentanaPrincipal.mainloop()

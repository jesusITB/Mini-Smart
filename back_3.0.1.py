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
            VentanaAdmin(Nombre_Sql_Resultado)
        elif Id_Usu == 'Alumno':
            VentanaUsuario(Nombre_Sql_Resultado,id_usuario_global)
        elif Id_Usu == 'Profe':
            VentanaProf(Nombre_Sql_Resultado)
    else:
        messagebox.showwarning("Lectura incorrecta",'Esta tarjeta no esta registrada en nuestro sistema, ponte en contacto con un administrador')

##########################################################################################################

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
    Button (VentAnd, text='Prueba2',width=25, height=15, command=partial(MenuListaDB, Nombre_Usuario),border=5).place(x=1590, y=650)

    #boton cerrar
    Button (VentAnd,text='X',command=VentAnd.destroy).place(x=1880,y=4)

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

    Label(VentAlt, width=10, height=5,text='correo').place(x=150,y=600)
    Entry(VentAlt,textvariable=correo).place(x=100,y=700)


    Label(VentAlt, width=10, height=5,text='nombre').place(x=500,y=600)
    Entry(VentAlt,textvariable=nombre).place(x=450,y=700)

    Label(VentAlt, width=10, height=5,text='apellido').place(x=150,y=800)
    Entry(VentAlt,textvariable=apellido).place(x=100,y=900)

    Label(VentAlt, width=10, height=5,text='tipo').place(x=850,y=800)
    ttk.Combobox (VentAlt,textvariable=tipo,state="readonly",values=[' ','Alumno', 'Profe', 'Administrador''']).place(x=800,y=700)

    Label(VentAlt, width=10, height=5,text='clase').place(x=850,y=600)
    ttk.Combobox (VentAlt,textvariable=clase,state="readonly",values=[' ', 'SMX1A', 'SMX1B', 'SMX1C', 'SMX1D', 'SMX1E', 'SMX1F', 'SMX2A', 'SMX2B', 'SMX2C', 'SMX2E', 'ASIXc1B', 'A3Dm1A', 'DAWe1A', 'DAMr1A', 'DAMi1A', 'DAMv1A', 'ASIXc2A', 'ASIXc2B', 'DAWe2A', 'DAMr2A', 'DAMi2A', 'DAMv2A', 'MMEIA', 'MMEIB', 'BATXd1A']).place(x=800,y=900)





    Label(VentAlt, width=10, height=5).place(x=500,y=800)


    
    #boton comprobar usuario
    Button (VentAlt, text='comprobar', width=400, height=400, image=img2, command=alta_Usuario,border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAlt,text='X',command=VentAlt.destroy).place(x=1880,y=4)



    VentAlt.mainloop()

def MenuAltaProduct(Nombre_Usuario):

    def alta_UsuarioProduct():
        global conexion
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
    FrameAltProduct.config(width=1980, height=520,bg='#e7dbcb')

    #frame2
    FrameAzul = Label(VentAltProducct, width=90, height=520, bg='red')
    FrameAzul.place(x=1300,y=520)

    Label(VentAltProducct,text=Nombre_Usuario,font=("Consolas", 20),bg='#e7dbcb').place(x=2,y=8)
    Label(VentAltProducct,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentAltProducct,text='Producto Alta',font=("Consolas", 17),bg='#e7dbcb').place(x=900,y=450)
    
    #varibles
    estado = StringVar()
    nombre = StringVar()
    precio = StringVar()
    tipo = StringVar()
    Descripcion = StringVar()
    solicitante = StringVar()

    Label(VentAltProducct, width=10, height=5,text='Nombre').place(x=150,y=600)
    Entry(VentAltProducct,textvariable=nombre).place(x=100,y=700)

    Label(VentAltProducct, width=10, height=5,text='Estado').place(x=500,y=600)
    ttk.Combobox(VentAltProducct,textvariable=estado,values=['','EN PERFECTO ESTADO','EN BUEN ESTADO','EN ESTADO NORMAL','EN MAL ESTADO' ,]).place(x=550,y=700)

    Label(VentAltProducct, width=10, height=5,text='precio').place(x=150,y=800)
    Entry(VentAltProducct,textvariable=precio).place(x=100,y=900)

    Label(VentAltProducct, width=10, height=5,text='tipo').place(x=500,y=800)
    ttk.Combobox (VentAltProducct,textvariable=tipo,state="readonly",values=['','Protector silicona','Estoig viatge','Ulleres VR Oculus Quest 2',
    'Comandaments consola','Webcam','Drons','Protector drons','Bateria drons','Tornavisos','Escanner de Barres','Adaptador USB-C','Gimbal',
    'Ulleres VR Pico Neo 3 pro','Ulleres VR- HP rever g2','Ulleres VR Microsoft Hololens','Pinça Onrobot Gripper', 'Raspberry pi 4','Raspberry pi 4',
    'Raspberry Pi 4 b 4Gb car','Raspberry Pi 4 b 4Gb','Rasperrry Pi 3 A','Raspberry pi 4',
    'Modulo GPS','Raspberry pi 4','Raspberry pi 4','Raspberry pi 4','Tauleta Wacom''Raspberry pi 4','Raspberry pi 4','Elego Starter Kit de Arduino',
    'arduino car','Raspberry pi 4','Raspberry pi 4','Raspberry pi 4','sensor infraroig','carcasa i rodes cotxe',
    'clauers RFID','GPS','WIFI ','sensor luz ',]).place(x=450,y=900)

    Label (VentAltProducct, width=10, height=5,text='descripcion').place(x=1140,y=600)
    Entry(VentAltProducct,textvariable=Descripcion).place(x=1000,y=700,width=350,height=250)

    Label (VentAltProducct, width=10, height=5,text='SOLICITANTE').place(x=800,y=800)
    Entry(VentAltProducct,textvariable=solicitante).place(x=800,y=900)

    
    #boton comprobar usuario
    Button (VentAltProducct, text='comprobar', width=400, height=400, image=img2, command=alta_UsuarioProduct,border=8).place(x=1420, y=600)

    #boton cerrar
    Button (VentAltProducct,text='X',command=VentAltProducct.destroy).place(x=1880,y=4)



    VentAltProducct.mainloop()

def MenuListaDB(Nombre_Usuario):
    cursor= conexion.cursor()


    def Eliminar():
        correo = lista.selection()[0]
        cursor.execute(f"DELETE FROM `Usuarios` WHERE `Usuarios`.`usu_correo` ='{correo}'")
        conexion.commit()
        lista.delete(correo)


    imgL = Image.open('/media/pi/KINGSTON/IA/image/LogoItb.png')
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

    Label(VentList,text=Nombre_Usuario,font=("Consolas", 20),bg='blue').place(x=10,y=8)
    Label(VentList,image=imagenMini,width=200,height=200,bg='#e7dbcb').place(x=1050,y=50) 
    Label(VentList,text='Lista',font=("Consolas", 17),bg='#e7dbcb').place(x=1115,y=250)

    lista = ttk.Treeview(VentList)
    lista.place(x=400,y=350)
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


    #boton
    Button(FrameAzul, text='Eliminar', command=lambda:Eliminar()).place(x=20,y=100)

    #boton
    Button(FrameAzul, text='vaciar', command=lambda:VaciaTabla()).place(x=20,y=300)




    #boton cerrar
    Button (VentList,text='X',command=VentList.destroy).place(x=1880,y=4)

    VentList.mainloop()

##########################################################################################################

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


#########################################################################################################

def VentanaUsuario(Nombre_Usuario,id_usuario_global):
    global imagentt
    global conexion
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
        def Ventana_float():
            #
            VentUsu=Toplevel()
            VentUsu.title('Smart-tacker')
            VentUsu.geometry('400x400')
            VentUsu.config(bg='#7B1FA2') #COLOR


        RetorUid  , text = reader.read()

        fecha_R= (date.date())
        #Ventana_float()
        try:
            cursor.execute(f"UPDATE `Prestamo` SET `pre_fecha_devolucion`='2022-12-1', `pre_activo`='No activo' WHERE `pro_id`='385898029682' AND `pre_activo`='Activo';")
            conexion.commit()

            cursor.execute(f"UPDATE Producto SET pro_disponibilidad='Disponible' WHERE pro_id='385898029682';")
            
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
    FrameBajo.config(width=1980, height=520,bg='#e7dbcb')

    #label
    Label(VentUsu,image=imagentt,width=250,height=250,bg='#e7dbcb').place(x=850,y=150) 
    Label(VentUsu,text='Alumno',font=("Consolas", 25),bg='#e7dbcb').place(x=920,y=450)
    Label (VentUsu,text=Nombre_Usuario,font=("Consolas", 20),bg='#e7dbcb').place(x=2,y=8)

    #boton 1
    imgPre = PhotoImage()
    Button (VentUsu,text='Prestamo',width=25, height=15,command=Prestamo,border=5).place(x=540, y=650)
    
    #boton 2
    Button (VentUsu, text='Retornar',width=25, height=15, command=Retornar,border=5).place(x=1150, y=650)

    #boton cerrar
    Button (VentUsu,text='X',command=VentUsu.destroy).place(x=1880,y=4)

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

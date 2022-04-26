#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#hombre : https://giphy.com/stickers/GrupoCorreos-correos-grupo-repartidor-WpC0MzuNNmbdSz0xwo
#chica : https://giphy.com/stickers/GrupoCorreos-cartera-correos-grupo-loLiRSeir4nxc5hW3s
#entregado y devuelto : https://giphy.com/stickers/transparent-Jho0wLvBNGOk4JCsFl
#guarda db : https://giphy.com/stickers/ivoymx-delivery-mensajeria-ivoy-KePwloRgQIkSX4wqIN

# tkinter
# https://github.com/ParthJadhav/Tkinter-Designer
# https://github.com/TomSchimansky/CustomTkinter
# https://github.com/Miraj50/Awesome-Tkinter-Apps
#
#






from ctypes import resize
from time import sleep
import tkinter as tk
from tkinter import PhotoImage, Toplevel, messagebox
from turtle import width
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from PIL import ImageTk, Image
import os

GPIO.setwarnings(False)
reader = SimpleMFRC522()

admin ="DEADG666D"
user = "user"
fran = "36002660484"

#validar tarjeta

def Validar_tarjeta():
    print ("Escaneando tarjeta")
    id, text = reader.read()
    print("ID: %s\nText: %s" % (id,text))
    if id == 385898029682:
        abrirventana1()
    elif id == 253300343202:
        ventanaAdmins()
    else:
        messagebox.showwarning("Lectura incorrecta",'Esta tarjeta no esta registrada en este sistema')

def EscribirTarjeta():
    try:
            text = input('New data:')
            print("Now place your tag to write")
            reader.write(text)
            print("Written")
    finally:
            GPIO.cleanup()

def ventanaAdmins():

    #ventana principal
    ventana1.withdraw() 
    win=Toplevel(ventana1)
    win.geometry('1920x1080') 
    win.title('Smart-tacker')
    win.configure(background='blue')
    e3=tk.Label(win,text =' bienvenido a la ventana de ADMIN', bg='red', fg='white')
    e3.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    botoncerrar=tk.Button(win, text='cerrar', command=ventana1.destroy)
    botoncerrar.pack(side=tk.TOP)

    #boton 1
    img1 = Image.open("/media/pi/KINGSTON/IA/image/NFC.jpeg")
    pequeñoimagen1 = img1.resize((100, 100))
    imagen1 = ImageTk.PhotoImage(pequeñoimagen1)
    buto1 = tk.Button(win, text='click me', image=imagen1).pack(padx=500, pady=350, ipadx=100, ipady=500)



    #boton 2
    img2 = Image.open("/media/pi/KINGSTON/IA/image/NFC.jpeg")
    pequeñoimagen2 = img2.resize((100, 100))
    imagen2 = ImageTk.PhotoImage(pequeñoimagen2)
    buto2 = tk.Button(win, text='click me', image=imagen2).pack()



    #boton 3
    img3 = Image.open("/media/pi/KINGSTON/IA/image/NFC.jpeg")
    pequeñoimagen3 = img3.resize((100, 100))
    imagen3 = ImageTk.PhotoImage(pequeñoimagen3)
    buto3 = tk.Button(win, text='click me', image=imagen3).pack()


    win.mainloop()

def abrirventana1():
    #cerrar ventana
    print('entre')
    ventana1.withdraw() 

    win=Toplevel(ventana1)
    #configurar la geometria-tamaño de la pantalla
    win.geometry('1920x1080') 

    win.title('smart')
    #configure (en este caso es el fondo)
    win.configure(background='blue')
    e3=tk.Label(win,text =' bienvenido a la ventana de USUARIO', bg='red', fg='white')
    #tamaño (.Pack)
    e3.pack(padx=5,pady=5,ipadx=5,ipady=5,fill=tk.X)
    #asignamos un boton la ventana (win) con el texto (OK)
    botoncerrar=tk.Button(win, text='regresar', command=ventana1)
    botoncerrar.pack(side=tk.TOP)


    #side es igual al lugar donde se situa el botton

    win.mainloop()




ventana1=tk.Tk()
ventana1.title("Smart")
ventana1.geometry('1920x1080')
ventana1.configure(background='blue')
botoncerrar=tk.Button(ventana1, text='cerrar', command=ventana1.destroy)
botoncerrar.pack(side=tk.TOP)

#boton
img = Image.open("/media/pi/KINGSTON/IA/image/NFC.jpeg")
pequeñoimagen = img.resize((1000, 800))
imagen = ImageTk.PhotoImage(pequeñoimagen)
buto = tk.Button(ventana1, text='click me', image=imagen, command=Validar_tarjeta).pack()




ventana1.mainloop()



#from time import sleep
#import sys
#import RPi.GPIO as GPIO
#from mfrc522 import SimpleMFRC522

#reader = SimpleMFRC522()


#try:
#        while True:
#                print ("Escaneando tarjeta")
#                id, text = reader.read()
#                print(id)
#                print(text)
#        
#                sleep(5)
#
#except KeyboardInterrupt:
#    GPIO.cleanup()
#    raise

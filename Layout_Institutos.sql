#Comando de pruebas
DROP DATABASE IF EXISTS DB_layout;

#Crear base de datos
CREATE DATABASE IF NOT EXISTS DB_layout;

#Usar la base de datos
USE DB_layout;

#Tablas sin relacion
CREATE TABLE IF NOT EXISTS Usuarios( #Tabla la cual almacena a los usuarios.
	usu_correo VARCHAR(320) NOT NULL, #Correo electrónico de la persona.
    usu_id BIGINT NOT NULL, #Id de la tarjeta nfc a la cual se va a vincular esta persona.
    usu_nombre VARCHAR(45) NOT NULL, #Nombre de la persona.
    usu_apellido VARCHAR(45) NOT NULL, #Apellido de la persona.
    usu_tipo ENUM('Alumno', 'Profe', 'Administrador') NOT NULL, #Tipo de usuario y permisos que tendra la persona.
    usu_clase ENUM('NULL', 'SMX1A', 'SMX1B', 'SMX1C', 'SMX1D', 'SMX1E', 'SMX1F', 'SMX2A', 'SMX2B', 'SMX2C', 'SMX2E', 'ASIXc1B', 'A3Dm1A', 'DAWe1A', 'DAMr1A', 'DAMi1A', 'DAMv1A', 'ASIXc2A', 'ASIXc2B', 'DAWe2A', 'DAMr2A', 'DAMi2A', 'DAMv2A', 'MMEIA', 'MMEIB', 'BATXd1A') NOT NULL, #Clase a la cual pertenece la persona, si es profe o otra cosa que no sea alumno sera NULL.
    PRIMARY KEY (usu_correo) 
);


CREATE TABLE IF NOT EXISTS producto( #Tabla en la cual se guardan los productos del almacén.
	pro_id INT NOT NULL AUTO_INCREMENT, #Id del producto para poder utilizarlo en la tabla prestamo.
    pro_nombre VARCHAR(45) NOT NULL, #Nombre del producto, ej: Raspberry pi 4, Oculus quest 2.
    pro_descripcion VARCHAR(45) NOT NULL, #Aqui se especifica si trae cargador, gamepad, etc...
    pro_familia VARCHAR(45) NOT NULL, #Tipo de producto, ej; Raspberry, Gafas VR, Arduino.
    pro_estado ENUM('EN PERFECTO ESTADO', 'EN BUEN ESTADO', 'EN ESTADO NORMAL', 'EN MAL ESTADO') NOT NULL, #Estado del producto.
    pro_fecha_compra DATE NOT NULL, #Fecha en la que se compro el producto, sirve para poder tener una guia de como de util a sido el producto.
    pro_precio FLOAT NOT NULL, #Precio de compra del producto.
    pro_solicitante_compra VARCHAR(45) NOT NULL, #Persona que ha solicitado la compra del producto.
    PRIMARY KEY (pro_id)
);

#Tabla master
CREATE TABLE IF NOT EXISTS Prestamo( #Tabla para guardar los presamos realizados.
	pre_id INT NOT NULL AUTO_INCREMENT, #Id de la tabla producto para poder tener los prestamos organizados.
    usu_correo VARCHAR(320) NOT NULL, #Correo electrónico de la persona, el cual esta vinculado con la tabla de Usuarios.
    pro_id INT NOT NULL, #Id del producto, este campo esta vinculado con la tabla Prestamo.
    pre_fecha_prestamo DATE NOT NULL, #Fecha del dia del prestamo.
    pre_fecha_devolucion DATE, #fecha del dia que se devuelve el producto
    pre_notas VARCHAR(420) NULL, #Notas sobre el prestamo, ej: se ha devuelto roto.
    PRIMARY KEY (pre_id), 
    FOREIGN KEY (usu_correo) REFERENCES Usuarios(usu_correo) ON UPDATE CASCADE, #vinculacion de la tabla Usuarios con esta, ademas cuenta con el ON UPDATE CASCADE que sirve para que cuando cambiemos algo en las otras tablas se cambie en esta.
    FOREIGN KEY (pro_id) REFERENCES producto(pro_id) ON UPDATE CASCADE  #vinculacion de la tabla Producto con esta, ademas cuenta con el ON UPDATE CASCADE que sirve para que cuando cambiemos algo en las otras tablas se cambie en esta.
);

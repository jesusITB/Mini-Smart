#Comando para pruebas.
DROP DATABASE IF EXISTS DB_layout_institutos;

#Crear base de datos
CREATE DATABASE IF NOT EXISTS DB_layout_institutos;

#Usar la base de dato
USE DB_layout_institutos;

#Tablas sin relacion
CREATE TABLE IF NOT EXISTS Usuarios( #Tabla la cual almacena a los usuarios.
	usu_correo VARCHAR(320) NOT NULL, #Correo electrónico de la persona.
    usu_id BIGINT NOT NULL, #Id de la tarjeta nfc.
    usu_nombre VARCHAR(45) NOT NULL, #Nombre de la persona.
    usu_apellido VARCHAR(45) NOT NULL, #Apellido de la persona.
    usu_tipo ENUM('Alumno', 'Profe', 'Administrador') NOT NULL, #Tipo de usuario y permisos que tendrá la persona.
    usu_clase ENUM('NULL', 'SMX1A', 'SMX1B', 'SMX1C', 'SMX1D', 'SMX1E', 'SMX1F', 'SMX2A', 'SMX2B', 'SMX2C', 'SMX2E', 'ASIXc1B', 'A3Dm1A', 'DAWe1A', 'DAMr1A', 'DAMi1A', 'DAMv1A', 'ASIXc2A', 'ASIXc2B', 'DAWe2A', 'DAMr2A', 'DAMi2A', 'DAMv2A', 'MMEIA', 'MMEIB', 'BATXd1A') NOT NULL, #Clase a la cual pertenece la persona, si es profe o admin será NULL.
    PRIMARY KEY (usu_correo) 
);

CREATE TABLE IF NOT EXISTS Producto( #Tabla en la cual se guardan los productos del almacén.
	pro_id BIGINT NOT NULL AUTO_INCREMENT, #Id del producto para poder utilizarlo en la tabla préstamo.
    pro_nombre VARCHAR(45) NOT NULL, #Nombre del producto, ej: Raspberry pi 4, Oculus quest 2.
    pro_descripcion VARCHAR(45) NOT NULL, #Aquí se especifica si trae cargador, gamepad, etc...
    pro_familia VARCHAR(45) NOT NULL, #Tipo de producto, ej; Raspberry, Gafas VR, Arduino.
    pro_estado ENUM('EN PERFECTO ESTADO', 'EN BUEN ESTADO', 'EN MAL ESTADO') NOT NULL, #Estado del producto.
    pro_fecha_compra DATE NOT NULL, #Fecha en la que se compró el producto, sirve para poder tener una guía de cómo de útil ha sido el producto.
    pro_precio FLOAT NOT NULL, #Precio de compra del producto.
    pro_solicitante_compra VARCHAR(45) NOT NULL, #Persona que ha solicitado la compra del producto.
    PRIMARY KEY (pro_id)
);

#Tabla master
CREATE TABLE IF NOT EXISTS Prestamo( #Tabla para guardar los préstamos realizados.
	pre_id INT NOT NULL AUTO_INCREMENT, #Id de la tabla producto para poder tener los préstamos organizados.
    usu_correo VARCHAR(320) NOT NULL, #Correo electrónico de la persona, el cual está vinculado con la tabla de Usuarios.
    pro_id BIGINT NOT NULL, #Id del producto, este campo está vinculado con la tabla Préstamo.
    pre_fecha_prestamo DATE NOT NULL, #Fecha del dia del préstamo.
    pre_fecha_devolucion DATE, #fecha del dia que se devuelve el producto
    pre_notas VARCHAR(420) NULL, #Notas sobre el préstamo, ej: se ha devuelto roto.
    PRIMARY KEY (pre_id), 
    FOREIGN KEY (usu_correo) REFERENCES Usuarios(usu_correo) ON UPDATE CASCADE, #vinculación de la tabla Usuarios con esta, además cuenta con el ON UPDATE CASCADE que sirve para que cuando cambiemos algo en las otras tablas se cambie en esta.
    FOREIGN KEY (pro_id) REFERENCES Producto(pro_id) ON UPDATE CASCADE  #vinculación de la tabla Producto con esta, además cuenta con el ON UPDATE CASCADE que sirve para que cuando cambiemos algo en las otras tablas se cambie en esta.
);

#Pruebas
INSERT INTO Usuarios (usu_correo, usu_id, usu_nombre, usu_apellido, usu_tipo, usu_departmento) VALUES
('Prueba@gmail.com', '253300243202', 'Francisco', 'Garcia', 'Administrador', 'Desarrollo'),
('Prueb2@gmail.com', '38589802968', 'Jesus', 'Gomez', 'Administrador', 'Desarrollo');

INSERT INTO Producto (pro_nombre, pro_descripcion, pro_familia, pro_estado, pro_fecha_compra, pro_precio, pro_solicitante_compra) VALUES
('Raspberry pi 4 B', 'Sin cargador', 'RASPBERRY', 'EN PERFECTO ESTADO', '2022-01-05', '101.99', 'Fernando Rivero'),
('Raspberry pi 3 A', 'Con gamepad', 'RASPBERRY', 'EN PERFECTO ESTADO', '2022-01-04', '151.99', 'Fernando Rivero');

INSERT INTO Prestamo (usu_correo, pre_fecha_prestamo, pro_id, pre_fecha_devolucion, pre_notas) VALUES
('Prueba@gmail.com', '2022-03-29', '1', '2022-03-30', 'Devuelto con todos los accesorios'),
('Prueba2@gmail.com', '2022-03-30', '2', '2022-03-31', 'Se ha devuelto con un arañazo en la parte superior de 3cm');


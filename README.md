# **_Mini-Smart™️_**
Este proyecto está enfocado en la administración y distribución de productos en las escuelas y empresas.

Consiste en una [raspberry pi 4](https://www.kubii.es/les-cartes-raspberry-pi/2772-nouveau-raspberry-pi-4-modele-b-4gb-kubii-0765756931182.html?src=raspberrypi) (Solamente ha sido probado en el modelo de 4GB) junto a un [lector RFID](https://www.amazon.es/Mifare-Tarjeta-Antena-lector-tarjetas/dp/B06X9PZSQN/ref=sr_1_6?__mk_es_ES=ÅMÅŽÕÑ&crid=JWRUNI69NF3Q&keywords=rc522&qid=1651066055&sprefix=rc+522%2Caps%2C83&sr=8-6) (Sirve cualquiera que sea RC-522).

![Raspberry RFID-RC522](https://user-images.githubusercontent.com/101580554/165537790-c2f83cf3-cb81-4aaf-b437-a7f9b4b68def.jpeg)

Para conectar el lector RFID-RC522 a la raspberry pi 4 será necesario conectar los pines de esta manera:
| Pines de la Raspberry | Pines del lector RFID-RC522 |
| ------------- | ------------- |
| [17] Rojo - 3v3 Power | [8] 3.3V |
| [18] Naranja - GPIO 23 / SPI3 CE1 N | [5] IRQ |
| [19] Amarillo - GPIO 10 / SPI0 MOSI / SDA5 | [4] MOSI |
| [20] Negro - Ground | [6] GND |
| [21] Azul - GPIO9 / SPI0 MISO / RXD4 | [3] MISO |
| [22] Morado - GPIO25 / SPI4 CE1 N | [7] RST |
| [23] Blanco - GPIO 11 / SPI0 SCLK / SCL5 | [2] SCK |
| [24] Verde - SDA4 / GPIO8 / SPI0 CE0 N / TXD4 | [1] SDA |

Además de necesitar **tarjetas o tags NFC** para poder guardar los datos del usuario.

![165322571-ab75bcc8-c726-4eb5-b56b-6f94f6329912](https://user-images.githubusercontent.com/101580554/165537817-226a83cd-fb4c-4958-aff6-c82373689162.jpg)

Luego, para tener los productos controlados se puede utilizar estas **pegatinas NFC** o se puede enganchar una tarjeta o tag al producto, también podría servir ese método.

![5157UyrS4jL _AC_SL1339_ (1)](https://user-images.githubusercontent.com/101580554/165537854-476a635f-7f34-4acb-9cd9-9bf136c8835e.jpg)

Gracias a una **base de datos** la cual estará en la raspberry, almacenara los datos de los **productos** además de los **usuarios creados** y los vinculara para hacer una lista de la gente a la que se le han prestado cosas, habrá dos tipos de base de datos, una para [empresas](https://github.com/jesusITB/Mini-Smart/blob/main/Layout_Empresas.sql) y otra para [centros educativos](https://github.com/jesusITB/Mini-Smart/blob/main/Layout_Institutos.sql).

## Configurar base de datos
Lo primero que tenemos que hacer es configurar la base de datos, lo primero de todo que tenemos que hacer es instalar MariaDB, para ello hacemos:
```
sudo apt update & sudo apt upgrade
```
Ahora, una vez que hemos actualizado el sistema, instalamos el paquete:
```
sudo apt install mariadb-server
```
Al descargarse el servicio de MariaDB se inicia automáticamente, podemos comprobarlo con:
```
sudo systemctl status mariadb
```
Si no está iniciado, solo tenemos que hacer el siguiente comando para iniciar el servicio:
```
sudo systemctl start mariadb
```

Una vez está instalado MariaDB tenemos que entrar a la base de datos como administrador, para hacerlo con poner **'sudo MariaDB'** o **'sudo MySQL'** bastaría, una vez estamos dentro tenemos que crear un usuario nuevo y darle permisos, el usuario de nuestra raspberry se llama pi (como la mayoría), así que este ejemplo lo haremos con ese usuario.
Para crearlo hacemos:
```
CREATE USER 'pi'@'localhost' IDENTIFIED BY '1234';
```
Para este ejemplo he puesto una contraseña fácil, pero se podría poner cualquiera que tú quisieras.

Para que ese usuario que acabamos de crear funcione tenemos que darle permisos, para darle permisos tenemos que poner:
```
GRANT ALL PRIVILEGES ON * . * TO 'pi'@'localhost';
```

Ahora, para que los cambios que acabamos de hacer funcionen, tenemos que volver a cargar los privilegios con:
```
FLUSH PRIVILEGES;
```
## Añadir el layout que prefiramos a la DB
Ahora viene lo más fácil, ya que tenemos las plantillas ya creadas, si se quiere modificar algo de ellas se puede, pero vas a tener que estar seguro del cambio y acordarte de cambiarlo en el código, solo recomiendo hacerlo si eres un usuario experimentado en MySQL y en Python, pero bueno, siempre podemos elegir o la de [Empresas](https://github.com/jesusITB/Mini-Smart/blob/main/Layout_Empresas.sql) o la de [Institutos](https://github.com/jesusITB/Mini-Smart/blob/main/Layout_Institutos.sql).

Ahora lo que tenemos que hacer es volver a iniciar sesion en MariaDB con **'sudo MariaDB'** o **'sudo MySQL'** y entraremos como administrador, para añadir cualquiera de los dos layouts es tan facil como copia y pegar todo el codigo en el shell de MariaDB,




Las librerias usadas son:

- from tkinter import *
- import RPi.GPIO as GPIO
- from mfrc522 import SimpleMFRC522
- from PIL import ImageTk, Image

El programa consiste en tres tipos de usuarios, en el caso de un instituto serian: **`Alumno`**, **`Profe`**, **`Admin`**, pero en caso de una empresa seria: **`User`**, **`Previligiados`**, **`Admin`**.

Lo primero que se ve al iniciar el programa es el **menú principal**, el boton que esta a la derecha es para empezar el escaneo de tarjetas.
![Menu principal](https://user-images.githubusercontent.com/101580554/167872099-9862923a-604a-4c2a-b04d-d5c184e68d3a.png)

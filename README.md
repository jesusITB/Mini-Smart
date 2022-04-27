# **_Mini-Smart™️_**
Este proyecto esta enfocado en la administracion y distribucion de productos en las escuelas y empresas.

Consiste en una [raspberry pi 4](https://www.kubii.es/les-cartes-raspberry-pi/2772-nouveau-raspberry-pi-4-modele-b-4gb-kubii-0765756931182.html?src=raspberrypi) (Solamente ha sido probado en el modelo de 4GB) junto a un [lector RFID](https://www.amazon.es/Mifare-Tarjeta-Antena-lector-tarjetas/dp/B06X9PZSQN/ref=sr_1_6?__mk_es_ES=ÅMÅŽÕÑ&crid=JWRUNI69NF3Q&keywords=rc522&qid=1651066055&sprefix=rc+522%2Caps%2C83&sr=8-6) (Sirve cualquiera que sea RC-522).

![Raspberry RFID-RC522](https://user-images.githubusercontent.com/101580554/165537790-c2f83cf3-cb81-4aaf-b437-a7f9b4b68def.jpeg)

Ademas de necesitar **tarjetas o tags NFC** para poder guardar los datos del usuario.

![165322571-ab75bcc8-c726-4eb5-b56b-6f94f6329912](https://user-images.githubusercontent.com/101580554/165537817-226a83cd-fb4c-4958-aff6-c82373689162.jpg)

Luego, para tener los productos controlados se puede utilizar estas **pegatinas NFC** o se puede enganchar una targeta o tag al producto, tambien podria servir.

![5157UyrS4jL _AC_SL1339_ (1)](https://user-images.githubusercontent.com/101580554/165537854-476a635f-7f34-4acb-9cd9-9bf136c8835e.jpg)
 
Gracias a una **base de datos** la cual estara en la raspberry, almacenara los datos de los **productos** ademas de los **usuarios creados** y los vinculara para hacer una lista de la gente a la que se le han prestados cosas, habra dos tipos de base de datos, una para empresas y otra para centros educativos.

El programa consiste en tres tipos de usuarios, en el caso de un instutito serian: `Alumno`, `Profe`, `Admin`, pero en caso de una empresa seria: `User`, `Previligiados`, `Admin`.

Para conectar el lector RFID-RC522 a la raspberry pi 4 sera necesario conectar los pins de esta manera:
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


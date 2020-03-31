Experimenting Tool with Design Patterns (Server Project)
--------------------------------------------------------
Este proyecto almacena los archivos, modulos y scripts del proyecto servidor
de una herramienta que permite experimentar con patrones de diseño. El proyecto 
Este proyecto contiene el script y modulos necesarios para realizar el manejo, clasificacion y redireccionamiento de los incidentes o vulnerabilidades en las cuales las direcciones de puntonet se ven involucradas

Antes de instalar
Este proyecto requiere de las siguientes dependencia. Alguna de ellas serán instaladas en el script de configuracion.

git*
python 3.5*
pip 3*
setuptools*
mysql - server*
mysql - client*
pandas**
sqlalchemy**
pymysql**
*Dependencias necesarias para correr el script de configuracionn. Instalarlas con:

Tambien se debe instalar el gestor de bases POSTGRES
apt-get install git

apt-get install python3-dev

apt-get install python3-pip

apt-get install mysql-server

apt-get install mysql-client
**Dependencias que seran instaladas dentro del proceso de configuración.

Descarga
El proyecto se encuentra el repositorio:

Manejo Incidentes

para descargarlo, acceder al enlace o en la consola usar el comando:

git clone https://github.com/JPuntoGuerra/ManejoIncidentes
Instalación
Una vez descargado el paquete es necesario configurar los datos sobre los cuales funcionará el programa. Para esto se puede abrir el archivo de configuración con algún editor de texto y añadir la información solicitada.

Finalmente para hacer periódico al programa se procedera a configurar un cronjob de la siguiente manera:

usuario@UbuntuIncidentes:~$ crontab -e
con este comando se abrirá el archivo de configuración de los cronjobs. En el se deberá añadir la siguiente linea.


tiempo/* * * * *  /path/directorio/ManejoIncidentes/script_incidentes.py >> /path/directorio/ManejoIncidentes/log.txt  

donde tiempo es un valor que indica cada cuantos minutos se repetirá el programa.
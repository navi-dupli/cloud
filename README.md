# Converter API

El propósito de esta API es permitir a usuarios de internet subir abiertamente diferentes formatos multimedia de archivos y cambiarles su formato o realizar procesos de compresión.

El modelo general de funcionamiento de la aplicación se basa en crear una cuenta en el portal web y acceder al administrador de archivos. Una vez la cuenta ha sido creada, el usuario puede subir archivos y solicitar el cambio de formato de estos para descargarlos. La aplicación permite a un usuario convertir archivos multimedia en línea de un formato a otro, seleccionando únicamente el formato destino.

En esta version a aplicación permite convertir entre los formatos de audio:

- MP3 - AAC - OGG - WAV – WMA

## Requisitos

Para poder correr correctamente la aplicación asegúrese de tener instalado lo siguiente:

- Git >= 2.24.3
- Python = 3.9
- Docker >= 20.10.12
- Docker-compose >= 1.29.2

### 1. Clonar el proyecto

Clone el proyecto con su software de confianza o ejecute en terminal

```bash
git clone https://github.com/navi-dupli/cloud.git &&  cd cloud
```

### 2. Construya las imagenes de docker

El proyecto está configurado para correr con contenedores de docker y tiene los siguientes servicios 

- Postgresql
- Redis
- Api-rest [Flask]
- Tareas [Celery] 

Todos los servicios mencionados anteriormente ya están configurados en el archivo ```docker-compose.yaml```

Tanto la aplicación en **Api-Rest con Flask** como con la aplicación **Tareas con Celery**, se construyen con el archivo ```DockerFile```

Haga el build corriendo lo siguiente en la terminal
```bash 
    docker-compose --profile all build
```

### 4. Correr el ambiente

Arranque el ambiente corriendo lo siguiente en la terminal
```bash 
    docker-compose --profile all up 
```
El comando anterior levantará 4 diferentes instancias en diferentes puertos de la siguiente manera:

- Postgresql (puerto: 5433)
- Redis (puerto: 6379)
- Api-rest [Flask] (puerto: 2000)
- Tareas [Celery]  (puerto 3000)

Para conectarse al postgresql requerirá datos adicionales como username, password, que encontrara en el archivo ```.env``` [ver variables POSTGRES_DB, POSTGRES_PASSWORD y POSTGRES_USER]

### 5. Probar el Api-Rest

Para probar el api rest puede hacer uso de la documentación propia del api Rest en postman

[Ver api en Postman](https://documenter.getpostman.com/view/8109655/2s84DrPMEr)



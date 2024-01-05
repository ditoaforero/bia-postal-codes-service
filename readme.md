# bia-postal-codes-service

## Descripcion
Este repositorio contiene únicamente los servicios necesarios para procesar los códigos postales.

## Instalación

### Requisitos previos

Install [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/), and [docker-compose](https://docs.docker.com/compose/install/).

### Configuración

Clone este repositorio y ejecute el docker-compose

```
git clone https://github.com/ditoaforero/bia-postal-codes-service.git
cd bia-postal-codes-service
docker-compose up -d
```
**Nota**: 
Para ampliar escalabilidad en la actualización de los codigos postales puedes adjuntar el parametro --scale coordinates=x donde x es el número de workers escuchando para procesar las peticiones
```
docker-compose up -d --scale coordinates=10
```

Una vez ejecutado el docker-compose, la API esta escuchando por el puerto 5000.

#### Endpoints disponibles

| Method | Endpoint | Descripcion                                                                     |
|--------| --------|---------------------------------------------------------------------------------|
| POST   | http://127.0.0.1:5000/coordinates    | Recibe el archivoCSV y guarda la informacion en Postgres                        |
| GET    | http://127.0.0.1:5000/calculate-postcode  | Procesa la informacion almacenada en Postgres actualizando los codigos postales |


## Ejecución de pruebas unitarias
``` bash
python -m unittest -vv src/tests/controller/test_app.py
```

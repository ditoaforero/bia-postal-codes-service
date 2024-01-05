# microservices-postal-codes

## Descripcion
Este proyecto contine los microservicios necesarios para processar los códigos postales.


## Instalación

### Requisitos previos

Install [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/), and [docker-compose](https://docs.docker.com/compose/install/).

### Configuración

Clone este repositorio y ejecute el docker-compose

```
git clone xxxxx
cd microservices-postal-codes
docker-compose up -d
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

---

---

# Instrucciones para acceso al cluster del CEDIA

Conectarse al HPC usando ssh: en windows se debe usar putty, en GNU/Linux se debe ssh en el terminal

```bash
ssh gabriel.gaona__ikiam.edu.ec@hpc.cedia.edu.ec
```

NOTA: Esto se debe hacer desde la computadora donde se creó la llave ssh de su usuario

# Reservar recursos para trabajar

Para reservar recursos para trabajar en el cluster del CEDIA se debe ejecutar el siguiente comando:

```bash
salloc -p cpu -n 2 -c 2  --mem=8GB --time=01:00:00
```

Si hay recusos disponibles y si la petición se ha hecho correctamente y existen los recursos disponibles en el cluster entces podrá ver un mensaje como el siguiente:

```
salloc: Pending job allocation 35713
salloc: job 35713 queued and waiting for resources
salloc: job 35713 has been allocated resources
salloc: Granted job allocation 35713
salloc: Waiting for resource configuration
salloc: Nodes dgx-node-0-0 are ready for job
```

Fíjese que la última línea indica el nodo que se ha asignado para que usted use. En este caso: "dgx-node-0-0"

# Ingresar al nodo asignado

Conéctese al nodo asignado usando ssh

```bash 
ssh dgx-node-0-0
```

# Crear una instancia de enroot para el modelo.

Esto se debe hacer una sola vez al inicio. Las siguientes ocasiones puedes saltarte estos pasos.

a. Importar imagen docker

```bash
enroot import docker://gabrielvgaona/curso-wrf:latest
```

b. Crear instancia WRF

```bash
enroot create --name wrf gabrielvgaona+curso-wrf+latest.sqsh
```

# Conectarse a la instancia del modelo.

```bash
enroot start --mount $HOME --root --rw wrf sh -c /bin/bash
```

Dentro de la instancia ya puedes instalar nano y descargar los scripts de datos

## Instalar nano

```bash
apt -y install nano
```

## Descargar los scripts de condiciones de borde

```bash
cd /home/gabriel.gaona__ikiam.edu.ec/
mkdir geodata/boundary-conditions/100
cd geodata/boundary-conditions/100
# descargar el listado de datos de condiciones de borde
wget -c https://raw.githubusercontent.com/gabrielvgaona/wrf-docker/refs/heads/main/home/rda-download_1.csh
# descargar los datos de condiciones de borde
csh rda-download_1.csh
```

Si quieres intentar resolver un ejercicio con mayor resolución puedes descargar estos datos:

NOTA: Esto no es necesario para el curso.

```bash
cd /home/gabriel.gaona__ikiam.edu.ec/
mkdir geodata/boundary-conditions/025
cd geodata/boundary-conditions/025
wget -c https://raw.githubusercontent.com/gabrielvgaona/wrf-docker/refs/heads/main/home/rda-download_0.25.csh
csh rda-download_1.csh
```

## Descargar datos geográficos para WPS

```bash
cd /home/gabriel.gaona__ikiam.edu.ec/geo_data
wget -c https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
tar -xvfz geog_high_res_mandatory.tar.gz
```

## Configurar WPS

Antes de modelar debemos configurar algunas cosas para el pre-procesamiento.

1. Configuración del `namelist.wps`

```bash
cd /WRF_ins/WPS
```

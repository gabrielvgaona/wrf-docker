
#####################

import os
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from wrf import getvar, to_np, ALL_TIMES
import xarray as xr
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import BoundaryNorm
import matplotlib.pyplot as plt
from netCDF4 import Dataset


# Configurar el directorio de archivos WRF
WRF_DIRECTORY = os.path.expanduser("/mnt/Data/geodata/ikiam/curso-wrf/wrfoutput")
WRF_FILES = sorted(glob(os.path.join(WRF_DIRECTORY, "wrfout_d03_*")))

# Asegurarse de que los archivos WRF existen
_WRF_FILES = [os.path.abspath(os.path.expanduser(f)) for f in WRF_FILES]
for f in _WRF_FILES:
    if not os.path.exists(f):
        raise ValueError(f"{f} no existe. Verifique el directorio o los nombres de archivo.")

# Función para obtener los archivos WRF
def multiple_wrf_files():
    return _WRF_FILES

# Extraer datos de los archivos WRF
file_paths = multiple_wrf_files()
wrf_files = [Dataset(f) for f in file_paths]

# Extraer precipitación acumulada
pre_wrf = getvar(wrf_files, "PREC_ACC_NC", timeidx=ALL_TIMES)[12:61,:,:]

# Obtener las coordenadas de latitud y longitud
lat = getvar(wrf_files, "XLAT")
lon = getvar(wrf_files, "XLONG")

# Convertir las variables a numpy arrays
lat = to_np(lat)
lon = to_np(lon)
################

# Cargar el archivo IMERG
ds = xr.open_dataset("imerg_event_20240615_tena.nc", engine='netcdf4')


theLats = ds['lat'].values
theLons = ds['lon'].values
x, y = np.float32(np.meshgrid(theLons, theLats))

pre_imerg =  ds['precipitation'][1:97,:,:]

### Media en el tiempo

mean_imerg = ds['precipitation'][1:97,:,:].mean(dim=('lat', 'lon'))

mean_wrf = pre_wrf.mean(dim=('south_north', 'west_east'))

######################
acum_imerg = mean_imerg.cumsum(dim='time').values 

# Obtener el tiempo para el eje x
time_imerg = mean_imerg['time'] # Ajusta según los datos disponibles

###############
acum_wrf= mean_wrf.cumsum(dim="Time").values

# Obtener el tiempo para el eje x
time_wrf = mean_wrf['Time']# Ajusta según los datos disponibles


############

# Graficar ambos promedios en un solo gráfico
plt.figure(figsize=(10, 6))

# Graficar IMERG (solo puntos de tiempo a 30 minutos)
plt.plot(time_imerg, mean_imerg, label='Acumulado IMERG', color='blue')

# Graficar WRF (solo puntos de tiempo a 1 hora)
plt.plot(time_wrf, mean_wrf, label='Acumulado WRF', color='red')

# Configuración del gráfico
plt.xlabel('Tiempo (Horas)')
plt.ylabel('Precipitación acumulada (mm)')
plt.title('Acumulado de Precipitación a lo largo del tiempo')
plt.legend()
plt.grid(True)

# Ajustar la visualización de las etiquetas del tiempo si es necesario
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar el gráfico
plt.show()


# Graficar ambos acumulados en un solo gráfico
plt.figure(figsize=(10, 6))

# Graficar IMERG (solo puntos de tiempo a 30 minutos)
plt.plot(time_imerg, acum_imerg, label='Acumulado IMERG', color='blue')

# Graficar WRF (solo puntos de tiempo a 1 hora)
plt.plot(time_wrf, acum_wrf, label='Acumulado WRF', color='red')

# Configuración del gráfico
plt.xlabel('Tiempo (Horas)')
plt.ylabel('Precipitación acumulada (mm)')
plt.title('Acumulado de Precipitación a lo largo del tiempo')
plt.legend()
plt.grid(True)

# Ajustar la visualización de las etiquetas del tiempo si es necesario
plt.xticks(rotation=45)
plt.tight_layout()

# Mostrar el gráfico
plt.show()


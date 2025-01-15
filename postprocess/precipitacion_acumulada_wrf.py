import os
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from wrf import getvar, to_np, ALL_TIMES

# Configurar el directorio de archivos WRF
WRF_DIRECTORY = os.path.expanduser("/mnt/Data/geodata/ikiam/curso-wrf/wrfoutput")
WRF_FILES = glob(os.path.join(WRF_DIRECTORY, "wrfout_d03_*"))

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
pre = getvar(wrf_files, "PREC_ACC_NC", timeidx=ALL_TIMES)

# Seleccionar el rango de tiempo deseado
pre_len = pre[1:48, :, :]

# Convertir la variable "Time" a formato datetime y sumar la precipitación
pre_len['Time'] = pd.to_datetime(pre_len['Time'].values)
pre = pre_len.sum(dim='Time')

# Obtener las coordenadas de latitud y longitud
lat = getvar(wrf_files, "XLAT")
lon = getvar(wrf_files, "XLONG")

# Convertir las variables a numpy arrays
lat = to_np(lat)
lon = to_np(lon)
pre = to_np(pre)


# Coordenadas de la Universidad IKIAM, 
x1, y1 =  -77.8626934,-0.9502232
name1 = "Universidad IKIAM"


# Coordenadas de la Universidad IKIAM, Cuenca, Ecuador
x2, y2 = -77.8159,-0.989
name2 = "Tena"

# Crear la figura y el eje con proyección PlateCarree
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()},
                       figsize=(14, 6))

# Configurar el dominio del mapa (modificar según el área de interés)
ax.set_extent([-78.4, -77.58, -1.3, -0.52], crs=ccrs.PlateCarree())

# Añadir el punto de la universidad al mapa y la leyenda
# Convertimos las coordenadas de la universidad a la misma proyección que el mapa

ax.scatter(x1, y1, color='green', zorder=20, 
           label=name1, transform=ccrs.PlateCarree())
ax.scatter(x2, y2, color='orange', zorder=20, 
           label=name2, transform=ccrs.PlateCarree())

# Añadir líneas de costa y cuadrícula
ax.coastlines(color='#969696')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, 
                  color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False
gl.right_labels = False


# Graficar la precipitación acumulada usando pcolormesh
sc_precip = ax.pcolormesh(lon, lat, pre, cmap='nipy_spectral', 
                          shading='auto', transform=ccrs.PlateCarree(),
                          vmin=0, vmax=300)

# Añadir una barra de color
cbar = plt.colorbar(sc_precip, ax=ax, orientation='vertical')
cbar.set_label('Precipitación Acumulada (mm)')

# Título del gráfico
ax.set_title(f'WRF Precipitación Acumulada (2024-06-15 a 2024-06-17)', fontsize=14)

# Añadir la leyenda
plt.legend()

# Mostrar el gráfico
plt.show()



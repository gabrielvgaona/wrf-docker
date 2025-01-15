#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 20:08:04 2025

@author: durdiale
"""

import os
from glob import glob
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib.colors import BoundaryNorm
import os
from glob import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from netCDF4 import Dataset
from wrf import getvar, to_np, ALL_TIMES


# Cargar el archivo IMERG
ds = xr.open_dataset("/mnt/Data/Desarrollo/wrf-docker/postprocess/imerg_event_20240615_tena.nc", engine='netcdf4')


theLats = ds['lat'].values
theLons = ds['lon'].values
x, y = np.float32(np.meshgrid(theLons, theLats))

precip_acumulated =  ds['precipitation'][1:97,:,:].sum(dim='time').values
precip_acumulated  = np.transpose(precip_acumulated)

# Coordenadas de la Universidad IKIAM, 
x1, y1 =  -77.8626934,-0.9502232
name1 = "Universidad IKIAM"


# Coordenadas de la Universidad IKIAM, Cuenca, Ecuador
x2, y2 = -77.8159,-0.989
name2 = "Tena"

# Crear la figura y el eje con proyección PlateCarree
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()},
                       figsize=(14, 6))

# Configurar el dominio del mapa (modificar según tu área de interés)
ax.set_extent([-78.4, -77.58, -1.3, -0.52], crs=ccrs.PlateCarree())

# Añadir el punto de la universidad al mapa y la leyenda
# Convertimos las coordenadas de la universidad a la misma proyección que el mapa

ax.scatter(x1, y1, color='green', zorder=20, label=name1, transform=ccrs.PlateCarree())
ax.scatter(x2, y2, color='orange', zorder=20, label=name2, transform=ccrs.PlateCarree())

# Añadir líneas de costa y cuadrícula
ax.coastlines(color='#969696')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False
gl.right_labels = False

# Graficar la precipitación acumulada usando pcolormesh
sc_precip = ax.pcolormesh(x, y, precip_acumulated, cmap='nipy_spectral', 
                          shading='auto', transform=ccrs.PlateCarree(),
                          vmin=0, vmax=300)

# Añadir una barra de color
cbar = plt.colorbar(sc_precip, ax=ax, orientation='vertical')
cbar.set_label('Precipitación Acumulada (mm)')

# Título del gráfico
ax.set_title(f'IMERG Precipitación Acumulada (2024-06-15 a 2024-06-17)', fontsize=14)

# Añadir la leyenda
plt.legend()

# Mostrar el gráfico
plt.show()



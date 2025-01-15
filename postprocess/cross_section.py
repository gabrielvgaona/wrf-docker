#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:25:11 2024

@author: durdiale
"""
import pandas as pd  # 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
from netCDF4 import Dataset
from wrf import getproj, get_cartopy


from wrf import to_np, getvar, CoordPair, vertcross


import os
from glob import glob

# This jupyter notebook command inserts matplotlib graphics in 
# to the workbook

# Modify these to point to your own files
WRF_DIRECTORY = os.path.expanduser("/mnt/Data/geodata/ikiam/curso-wrf/wrfoutput")
WRF_FILES = glob(os.path.join(WRF_DIRECTORY, "wrfout_d03_*"))


import numpy as np
from matplotlib import pyplot
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
from netCDF4 import Dataset
from wrf import (getvar, to_np, get_cartopy, latlon_coords, vertcross,
                 cartopy_xlim, cartopy_ylim, interpline, CoordPair)

from wrf import getvar, CoordPair, vertcross, latlon_coords, get_cartopy

import cartopy.crs as ccrs
from wrf import getvar


from wrf import (getvar, interplevel, vertcross, 
                 CoordPair, ALL_TIMES, to_np,
                 get_cartopy, latlon_coords,
                 cartopy_xlim, cartopy_ylim)

_WRF_FILES = [os.path.abspath(os.path.expanduser(
    os.path.join(WRF_DIRECTORY, f))) for f in WRF_FILES]

# Check that the WRF files exist
for f in _WRF_FILES:
    if not os.path.exists(f):
        raise ValueError("{} does not exist. "
            "Check for typos or incorrect directory.")

# Create functions so that the WRF files only need
# to be specified using the WRF_FILES global above
def single_wrf_file():
    global _WRF_FILES
    return _WRF_FILES[0]

def multiple_wrf_files():
    global _WRF_FILES
    return _WRF_FILES

print("All tests passed!")


from netCDF4 import Dataset
import numpy as np
import pandas as pd
from wrf import (getvar, CoordPair, vertcross, to_np, interpline, latlon_coords, get_cartopy)
import matplotlib.pyplot as pyplot

####################
# Cargar archivos WRF
####################
file_paths = multiple_wrf_files()  # Lista de archivos WRF
wrf_files = [Dataset(f) for f in file_paths]

# Definir sección transversal
cross_start = CoordPair(lat=-0.6, lon=-78.3)  # Cerro Paraguillas
cross_end = CoordPair(lat=-1.1, lon=-77.7)  # Limón Indanza

# Variables de WRF
ht = getvar(wrf_files, "z", timeidx=ALL_TIMES, units="m")[1:48, :, :]
ht['Time'] = pd.to_datetime(ht['Time'].values)
ht = ht.mean(dim='Time')

ter = getvar(wrf_files, "ter", timeidx=ALL_TIMES)
ter['Time'] = pd.to_datetime(ter['Time'].values)
ter = ter.mean(dim='Time')

rh_len = getvar(wrf_files, "PREC_ACC_NC", timeidx=ALL_TIMES)
rh_len= rh_len[1:48, :, :] 

rh = getvar(wrf_files, "rh", timeidx=ALL_TIMES)[1:48, :, :]
rh['Time'] = pd.to_datetime(rh['Time'].values)
rh = rh.mean(dim='Time')

w = getvar(wrf_files, "wa", timeidx=ALL_TIMES, units="m/s")[1:48, :, :]
w['Time'] = pd.to_datetime(w['Time'].values)
w = w.mean(dim='Time')

u = getvar(wrf_files, "ua", timeidx=ALL_TIMES, units="m/s")[1:48, :, :]
u['Time'] = pd.to_datetime(u['Time'].values)
u = u.mean(dim='Time')

# Cálculo de secciones transversales
rh_cross = vertcross(rh, ht, wrfin=wrf_files,
                     start_point=cross_start, end_point=cross_end,
                     latlon=True, meta=True)

w_cross = vertcross(w, ht, wrfin=wrf_files,
                    start_point=cross_start, end_point=cross_end,
                    latlon=True, meta=True)

u_cross = vertcross(u, ht, wrfin=wrf_files,
                    start_point=cross_start, end_point=cross_end,
                    latlon=True, meta=True)

# Rellenar valores faltantes en las secciones transversales
def fill_missing(cross_data):
    filled = np.ma.copy(to_np(cross_data))
    for i in range(filled.shape[-1]):
        column_vals = filled[:, i]
        first_idx = int(np.transpose((column_vals > -100).nonzero())[0])
        filled[0:first_idx, i] = filled[first_idx, i]
    return filled

rh_cross_filled = fill_missing(rh_cross)
w_cross_filled = fill_missing(w_cross)
u_cross_filled = fill_missing(u_cross)

# Línea del terreno
ter_line = interpline(ter, wrfin=wrf_files, start_point=cross_start,
                      end_point=cross_end)

# Coordenadas lat/lon
coord_pairs = to_np(rh_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])

# Formatear las etiquetas de las coordenadas con un decimal
x_labels = ["{:.1f}, {:.1f}".format(pair.lat, pair.lon) for pair in coord_pairs]

# Crear figura
fig = pyplot.figure(figsize=(10, 6))
ax_cross = pyplot.axes()

# Graficar humedad relativa (RH)
rh_levels = np.linspace(0, 100, 21)  # Niveles de humedad relativa (0-100%)
rh_contours = ax_cross.contourf(
    np.arange(rh_cross.shape[-1]),
    to_np(rh_cross.coords["vertical"]),
    to_np(rh_cross_filled),
    levels=rh_levels,
    cmap='Blues',
    extend="neither"  # Ajuste para que la barra de color no tenga puntas
)

# Barra de color para humedad relativa
cbar = fig.colorbar(rh_contours, ax=ax_cross, extend='neither')  # No tiene puntas
cbar.ax.tick_params(labelsize=12)

# Especificar las fechas de interés
start_date = str(rh_len['Time'].values[0])[:10]
end_date = str(rh_len['Time'].values[-1])[:10]
 

# Configurar las etiquetas de la barra de color de 10 en 10
cbar.set_ticks(np.arange(0, 101, 10))  # Establecer los ticks de 0 a 100, cada 10 unidades
cbar.set_label('Relative Humidity (%)', rotation=-270, fontsize=16)

cbar.ax.tick_params(labelsize=14)

# Rellenar el terreno
ht_fill = ax_cross.fill_between(
    np.arange(rh_cross.shape[-1]), 0, to_np(ter_line),
    facecolor="black"  # Usar el color saddle brown
)

# Aumentar la densidad de flechas
quiver = ax_cross.quiver(
    np.arange(0, u_cross_filled.shape[-1], 1),  # Reducir el paso de 2 a 1
    to_np(rh_cross.coords["vertical"]),
    to_np(u_cross_filled[:, :]),  # Usar toda la matriz para u
    to_np(w_cross_filled[:, :]) * 110,  # Usar toda la matriz para w y escalar
    scale=300, width=0.003
)
# Agregar la clave de quiver
ax_cross.quiverkey(
    quiver,
    X=0.15, Y=0.15,  # Posición en la esquina superior izquierda
    U=10,  # Velocidad de referencia
    label="10 (m/s⁻¹)", labelpos='E', coordinates='axes',
    fontproperties={'size': 14, 'weight': 'bold'},  # Texto resaltado
    color='white',  # Color de las flechas
    edgecolor='white',  # Borde blanco alrededor
    labelcolor='white',  # Color blanco para el valor "10 m s⁻¹"
    zorder=3  # Para que esté encima de las flechas
)
# Configuración de ejes
num_ticks = 6
thin = int((len(x_ticks) / num_ticks) + 0.6)
ax_cross.set_xticks(x_ticks[::thin])
ax_cross.set_xticklabels(x_labels[::thin], rotation=45, fontsize=16)
ax_cross.set_xlabel("Latitud, Longitud", fontsize=16)
ax_cross.set_ylabel("Elevation (m)", fontsize=16)
ax_cross.set_ylim(0, 6000)
# Obtener los valores de los ticks actuales del eje y
yticks = ax_cross.get_yticks()

# Filtrar los valores de los ticks, eliminando los que no deseas (por ejemplo, los valores decimales)
yticks_filtered = [tick for tick in yticks if tick.is_integer()]  # Filtrar para solo mostrar enteros

# Establecer los valores de los ticks filtrados
ax_cross.set_yticks(yticks_filtered)

# Establecer las etiquetas de los ticks, manteniendo el tamaño de fuente deseado
ax_cross.set_yticklabels([str(int(tick)) for tick in yticks_filtered], fontsize=16)

#Título de cada subgráfico
ax_cross.set_title(f"{start_date} to {end_date}", fontsize=16)


# Mostrar gráfico
pyplot.show()

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from __future__ import print_function
import os
from glob import glob

# Modify these to point to your own files
WRF_DIRECTORY = "/mnt/Data/geodata/ikiam/curso-wrf/wrfoutput" # mine is "/Users/misi1684/wrf_python_tutorial/wrf_tutorial_data"
WRF_FILES = glob(os.path.join(WRF_DIRECTORY, "wrfout_d03_*"))

#------------------------------------------------------
# Turn off annoying warnings
import warnings
warnings.filterwarnings('ignore')

# Make sure the environment is good
import numpy as np
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from cartopy import crs
from cartopy.feature import NaturalEarthFeature
import matplotlib
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import xarray as xr
import os
import matplotlib.colors as mcolors
import pandas as pd  # 
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib as mpl
from matplotlib import cm



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

################
# Extract data from WRF files
file_paths = multiple_wrf_files()
wrf_files = [Dataset(f) for f in file_paths]


pressure = getvar(wrf_files, "pressure", timeidx=ALL_TIMES)
z = getvar(wrf_files, "z", timeidx=ALL_TIMES, units="dm")
ua = getvar(wrf_files, "ua", timeidx=ALL_TIMES, units="m/s")
va = getvar(wrf_files, "va", timeidx=ALL_TIMES, units="m/s")
wspd = getvar(wrf_files, "wspd_wdir", timeidx=ALL_TIMES, units="m/s")[0, :]
pre = getvar(wrf_files, 'PREC_ACC_NC', timeidx=ALL_TIMES)

# Interpolate to 850 hPa
ht_850 = interplevel(z, pressure, 598)
u_850 = interplevel(ua, pressure, 598)
v_850 = interplevel(va, pressure, 598)
wspd_850 = interplevel(wspd, pressure, 598)

# Subset the data (for region of interest)
ht_850 = ht_850[35:61,:,:]
u_850 = u_850[35:61,:,:]
v_850 = v_850[35:61,:,:]
wspd_850 = wspd_850[35:61,:,:]
pre = pre[35:61,:,:]


pre['Time'] = pd.to_datetime(pre['Time'].values)
pre_hourly_mean = pre.groupby('Time.hour').mean(dim='Time')

wspd_850['Time'] = pd.to_datetime(pre['Time'].values)
wspd_850_hourly_mean = pre.groupby('Time.hour').mean(dim='Time')

v_850['Time'] = pd.to_datetime(pre['Time'].values)
v_850_hourly_mean = pre.groupby('Time.hour').mean(dim='Time')

u_850['Time'] = pd.to_datetime(pre['Time'].values)
u_850_hourly_mean = pre.groupby('Time.hour').mean(dim='Time')

ht_850['Time'] = pd.to_datetime(pre['Time'].values)
ht_850_hourly_mean = pre.groupby('Time.hour').mean(dim='Time')

# Get lat/lon coordinates using ht_850
lats, lons = latlon_coords(ht_850)

# Get the map projection information using ht_850
cart_proj = get_cartopy(ht_850)

# Crear una figura con una matriz 4x6 de subgráficas
fig, axes = plt.subplots(nrows=4, ncols=6, figsize=(18, 14), 
                         subplot_kw={'projection': cart_proj})

# Flatten la matriz de ejes para iterar sobre ellos
axes = axes.flatten()

# Crear una figura con 4x6 subgráficas
fig, axes = plt.subplots(nrows=4, ncols=6, figsize=(18, 12), subplot_kw={'projection': ccrs.PlateCarree()})

# Definir los grupos de horas
hour_groups = [(0, 5), (6, 11), (12, 17), (18, 23)]

# Crear las figuras para cada grupo de horas
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10), 
                         subplot_kw={'projection': ccrs.PlateCarree()})

axes = axes.flatten()  # Asegurar que los ejes estén en una lista manejable

for idx, (start, end) in enumerate(hour_groups):
    ax = axes[idx]  # Seleccionar el eje correspondiente
    
    ax.set_extent([-78.4, -77.58, -1.3, -0.52], crs=ccrs.PlateCarree())

    # Calcular los promedios acumulados para el rango de horas
    precip_mean = np.mean(pre_hourly_mean[start:end + 1, :, :], axis=0)
    u_wind_mean = np.mean(u_850_hourly_mean[start:end + 1, :, :], axis=0)
    v_wind_mean = np.mean(v_850_hourly_mean[start:end + 1, :, :], axis=0)

    # Añadir costas a la proyección
    ax.coastlines(color='#969696', linewidth=0.8)

    # Añadir la precipitación como contornos rellenos
    levels = np.arange(0., 22., 2.)  # Define los niveles de precipitación (ajústalos según los datos)
    precip_contours = ax.contourf(lons,
                                  lats,
                                  precip_mean,  # Promedio acumulado
                                  levels=levels,
                                  cmap="Blues",  # Usamos una paleta de colores que refleje precipitación
                                  zorder=0,
                                  transform=ccrs.PlateCarree())

    # Añadir las flechas de viento (dirección y velocidad) encima de la precipitación
    thin = [int(x / 10.) for x in lons.shape]  # Cada cuántos puntos colocar las flechas
    quiver = ax.quiver(to_np(lons[::thin[0], ::thin[1]]),
                       to_np(lats[::thin[0], ::thin[1]]),
                       to_np(u_wind_mean[::thin[0], ::thin[1]]),
                       to_np(v_wind_mean[::thin[0], ::thin[1]]),
                       scale=100,  # Ajusta el tamaño general de las flechas
                       color='black',  # Color de las flechas
                       width=0.005,  # Grosor de las flechas
                       headwidth=10,  # Aumento del tamaño de la cabeza de flecha
                       headlength=12,  # Aumento de la longitud de la cabeza de flecha
                       headaxislength=10)  # Aumento de la longitud del eje de la cabeza

    # Añadir una flecha de referencia solo en el primer subgráfico
    if idx == 0:
        ax.quiverkey(quiver,
                     X=0.15, Y=0.95,  # Posición en la esquina superior izquierda
                     U=10,  # Velocidad de referencia
                     label="10 m s⁻¹", labelpos='E', coordinates='axes',
                     fontproperties={'size': 14, 'weight': 'bold'},  # Texto resaltado
                     color='blue',  # Color azul para la flecha
                     edgecolor='black',  # Borde negro alrededor
                     zorder=3)  # Para que esté encima de las flechas

    # Añadir las líneas de la cuadrícula de latitud/longitud
    gridlines = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, color='gray', alpha=0.5, linestyle='--')

    # Desactivar etiquetas en la parte superior y derecha
    gridlines.top_labels = False
    gridlines.right_labels = False

    # Dejar solo etiquetas en la parte izquierda y en la parte inferior
    if idx % 2 == 0:
        gridlines.left_labels = True
    else:
        gridlines.left_labels = False
    if idx >= 2:
        gridlines.bottom_labels = True
    else:
        gridlines.bottom_labels = False

    # Ajustar el tamaño de las etiquetas de latitud y longitud
    gridlines.xlabel_style = {'size': 14}  # Tamaño de la fuente de las etiquetas de latitud
    gridlines.ylabel_style = {'size': 14}  # Tamaño de la fuente de las etiquetas de longitud

    # Añadir el texto como leyenda en la parte inferior izquierda
    ax.text(0.02, 0.04, f"from:{start:02d} to {end:02d}", 
            transform=ax.transAxes, fontsize=15, color="black",
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.2'))  # Añadido borde negro

# Ajustar los espacios entre las subgráficas para dejar poco espacio
plt.subplots_adjust(wspace=0.05, hspace=0.02)  # Ajustar los espacios entre las subgráficas

# Añadir una barra de colores compartida (vertical, derecha de todos los gráficos)
cbar = fig.colorbar(precip_contours, ax=axes, orientation="vertical", 
                    pad=0.02, shrink=0.8)

# Ajustar el tamaño de los números de los ticks de la barra de colores
cbar.ax.yaxis.set_tick_params(labelsize=18)  # Cambia a 16 o el tamaño que desees

cbar.set_label("Rainfall rate (mm h⁻¹)", fontsize=20)  # Cambio realizado aquí
cbar.ax.tick_params(fontsize=20)

# Ajustar los espacios entre subgráficas
plt.tight_layout()

# Mostrar la figura
plt.show()

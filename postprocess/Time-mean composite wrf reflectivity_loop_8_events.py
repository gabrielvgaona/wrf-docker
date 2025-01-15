#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 23:25:20 2024

@author: durdiale
"""

#######################
import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from pyproj import Proj, transform, CRS
from matplotlib_scalebar.scalebar import ScaleBar
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# Configuración base
base_path = os.path.expanduser('~/Documents/Script_WRF/2. wrf_reflectivity/data/550_650hpa/new')  # Expandir ~ a la ruta completa
event_folders = [f for f in os.listdir(base_path) if f.startswith('event_')]  # Buscar todas las carpetas que comienzan con "event_"

# Ordenar las carpetas de eventos por fecha (asumiendo que el formato del nombre es 'event_YYYYMMDD')
event_folders.sort(key=lambda x: x.split('_')[1])  # Ajusta el índice si el formato es diferente

# Coordenadas del punto central (Cuenca, Ecuador)
x_central, y_central = -79.24623, -2.75992
radius_km = 40
radius_deg = radius_km / 111.32  # Aproximación: 1° ≈ 111.32 km

# Definir las proyecciones
lat_lon_proj = Proj(CRS.from_epsg(4326))  # WGS84
utm_proj = Proj(CRS.from_epsg(32717))    # UTM zona 17S (Cuenca, Ecuador)

# Crear figura general
fig, axes = plt.subplots(3, 4, figsize=(10, 7), subplot_kw={'projection': ccrs.PlateCarree()})
axes = axes.flatten()  # Convertir en lista para iterar fácilmente

# Rango de niveles para la barra de color
color_levels = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5,
                2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5, 6,7,8,9,10,11,12,13,14,15]

# Procesar cada evento
for i, event_folder in enumerate(event_folders):
    if i >= len(axes):  # Evitar más subplots de los necesarios
        break

    # Construir la ruta de la carpeta
    folder_path = os.path.expanduser(os.path.join(base_path, event_folder))

    # Buscar automáticamente el archivo .nc en la carpeta
    nc_files = [f for f in os.listdir(folder_path) if f.endswith('.nc')]
    if len(nc_files) == 0:
        print(f"No se encontraron archivos .nc en {folder_path}")
        continue

    # Usar el primer archivo encontrado
    nc_file_path = os.path.join(folder_path, nc_files[0])
    print(f"Procesando archivo: {nc_file_path}")

    # Leer el archivo .nc usando xarray
    dataset = xr.open_dataset(nc_file_path, engine='netcdf4')
    
    # Aplicar un límite inferior a los valores de SndBZ
    dataset['dbz'] = dataset['dbz'].clip(min=0)

    # Filtrar los tiempos usando índices
    sndbz_mean = dataset['dbz'].isel(Time=slice(13, 61)).mean(dim='Time')
    
    # Coordenadas y datos
    lon, lat = dataset['XLONG'].values, dataset['XLAT'].values
    sndbz_data = sndbz_mean.values

    # Calcular la distancia desde el punto central
    distance = np.sqrt((lon - x_central) ** 2 + (lat - y_central) ** 2)

    # Crear una máscara para los datos dentro del círculo
    mask = distance <= radius_deg
    sndbz_data_cropped = np.where(mask, sndbz_data, np.nan)
    
    # Definir límites basados en el radio
    lon_min = x_central - radius_deg
    lon_max = x_central + radius_deg
    lat_min = y_central - radius_deg
    lat_max = y_central + radius_deg

    # Crear el subplot para el evento actual
    ax = axes[i]

    # Ajustar la extensión del mapa para que cubra el círculo
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

    # Añadir líneas de costa
    ax.coastlines(color='#969696')

    # Añadir un mesh plot al subplot
    sc = ax.contourf(lon, lat, sndbz_data_cropped,
                     levels=color_levels,
                     cmap='nipy_spectral', transform=ccrs.PlateCarree())

    # Configurar gridlines y etiquetas
    gl = ax.gridlines(draw_labels=True, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    # Deshabilitar etiquetas de la izquierda excepto en la primera columna
    if i % 4 != 0:  
        gl.left_labels = False

    # Deshabilitar etiquetas de abajo excepto en la última fila
    if i < len(event_folders) - 4:  # Si no está en la última fila
         gl.bottom_labels = False

    # Añadir un círculo al mapa
    circle = plt.Circle((x_central, y_central), radius_deg, edgecolor='black', facecolor='none', lw=1, transform=ccrs.PlateCarree())
    ax.add_patch(circle)

    # Título del subplot con el nombre posterior a "event_"
    event_title = event_folder.split('event_')[1]  # Obtener la parte después de "event_"
    ax.set_title(f'{event_title}', fontsize=11)  # Usar la parte extraída como título
    
    # Agregar la barra de escala solo en el primer gráfico
    if i == 0:  # Solo en el primer gráfico
        distance_in_meters = radius_km * 2000  # Radio en metros
        scalebar = ScaleBar(distance_in_meters, location='lower left', length_fraction=0.1, scale_loc='bottom', units='m', font_properties={'size': 12},
                            box_alpha=0.7)
        ax.add_artist(scalebar)

# Eliminar subplots vacíos
for j in range(len(event_folders), len(axes)):
    fig.delaxes(axes[j])

fig.suptitle('Simulated-WRF_YS (650-550 hPa)', fontsize=18, fontweight='bold')

fig.subplots_adjust(hspace=0.0001, wspace=0.001)
fig.tight_layout(pad=1.0) 

# Añadir una barra de color global
cbar = fig.colorbar(sc, ax=axes, orientation='horizontal', fraction=0.05, pad=0.1, aspect=30)
cbar.set_label('Time-mean composite WRF reflectivity (dBZ)', fontsize=20)
cbar.ax.tick_params(labelsize=14)
cbar.set_ticks([0, 1, 2, 3, 4, 5, 6,7,8,9,10,11,12,13,14,15])

# Guardar la figura general
WRF_RESULTS = os.path.expanduser("~/Documents/Script_WRF/results_december_2024")
output_path = os.path.join(WRF_RESULTS, "Simulated-WRF_YS_550_650hpa_best_simulations_new_40.jpeg")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"Gráfico combinado guardado en: {output_path}")

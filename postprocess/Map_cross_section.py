import os
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
from glob import glob
from wrf import (getvar, to_np, latlon_coords, get_cartopy, 
                 CoordPair, interplevel, ALL_TIMES)

# Modify these to point to your own files
WRF_DIRECTORY = os.path.expanduser("/mnt/Data/geodata/ikiam/curso-wrf/wrfoutput")
WRF_FILES = glob(os.path.join(WRF_DIRECTORY, "wrfout_d03_*"))

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

file_paths = multiple_wrf_files()  # Lista de archivos WRF
wrf_files = [Dataset(f) for f in file_paths]
temp = getvar(wrf_files, "temp", timeidx=ALL_TIMES, units="degC")[1:48, :, :]

# Abrir el archivo NetCDF
ncfile = Dataset("/mnt/Data/geodata/ikiam/curso-wrf/wrfoutput/wrfout_d01_2024-06-16_15:00:00")



# Obtener datos del terreno
temp = getvar(ncfile, "temp", timeidx=0, units="degC")[1:48, :, :]
temp_500 = temp[0,:,:]

# Definir la línea de sección transversal
cross_start = CoordPair(lat=-0.6, lon=-78.3)  # Tena
cross_end = CoordPair(lat=-1.1, lon=-77.7)  # Chalupas

# Coordenadas de Tena
xA, yA = -78.3, -0.6  # Coordenadas de Tena, Ecuador
nameA = "A"  # Nombre del punto


# Coordenadas de Chalupas
xB, yB = -77.7, -1.1  # RBCC
nameB = "B"  # Nombre del punto


# Coordenadas de Cuenca
x, y = -77.8159,-0.989
name = "Tena"  # Nombre del punto

# Obtener las coordenadas
lats, lons = latlon_coords(temp_500)
cart_proj = get_cartopy(temp_500)

# Crear figura y eje con la proyección adecuada
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": cart_proj})

# Dibujar el terreno como contorno
ter_contour = ax.contourf(to_np(lons), to_np(lats), to_np(temp_500),
                          levels=np.arange(5, 25, 1), cmap="terrain", transform=ccrs.PlateCarree())
cbar = plt.colorbar(ter_contour, ax=ax, orientation="vertical", pad=0.05)
cbar.set_label("Temperature (°C)", fontsize=20)  # Tamaño más grande del título
cbar.ax.tick_params(labelsize=14)  # Ajustar el tamaño de las etiquetas numéricas

# Dibujar la línea de la sección transversal
ax.plot([cross_start.lon, cross_end.lon], [cross_start.lat, cross_end.lat],
        color="black", linewidth=2, marker="o", transform=ccrs.PlateCarree(), label="Sección transversal")

# Configurar la extensión del mapa (parte de Sudamérica)
ax.set_extent([-78.4, -77.58, -1.3, -0.52], crs=ccrs.PlateCarree())

# Añadir líneas de costa y cuadrículas
ax.coastlines(color='#969696')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False
gl.right_labels = False

# Estilo de las etiquetas de latitud y longitud
gl.xlabel_style = {'size': 15}
gl.ylabel_style = {'size': 15}

# Añadir características adicionales del mapa
ax.add_feature(cfeature.BORDERS, linewidth=0.5)

# Graficar el punto de Cuenca después de definir el mapa y la proyección
ax.scatter(x, y, color='blue', zorder=15, transform=ccrs.PlateCarree())  # Ajustar el color y el zorder

# Añadir una etiqueta cerca del punto
plt.text(x - 0.01, y - 0.09, name, color='blue', fontsize=20, transform=ccrs.PlateCarree())

plt.text(xA - 0.01, yA + 0.05, nameA, color='black', fontsize=20, transform=ccrs.PlateCarree())

plt.text(xB - 0.01, yB + 0.05, nameB, color='black', fontsize=20, transform=ccrs.PlateCarree())



# Mostrar figura
plt.show()


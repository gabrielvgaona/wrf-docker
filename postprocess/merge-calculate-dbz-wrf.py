
def extract_first_and_last_date_from_netcdf(netcdf_file):
    # Extract the last date from the timestamp of the NetCDF data.
    ds = xr.open_dataset(netcdf_file,engine='netcdf4')
    # Check if 'time' coordinate exists
    if 'time' in ds.coords:
        # Assuming 'time' is a datetime64 coordinate
        first_date = ds['time'].values[0] 
        last_date = ds['time'].values[-1]  # Get the last timestamp
        return str(first_date)[:10],str(last_date)[:10] 
    else:
        raise ValueError("No 'time' coordinate found in the dataset.")
    ds.close()
def sort_wrfout_filenames(filenames):
    # Define a key function to extract the date and time from the filenames
    def extract_datetime(filename):
        # Extract the part of the filename that contains the date and time
        datetime_str = filename.split('_')[2:]  # Split and take the date and time parts
        datetime_str = '_'.join(datetime_str)  # Join back to a string
        return datetime.strptime(datetime_str, "%Y-%m-%d_%H:%M:%S")  # Convert to datetime object
    # Sort the filenames using the extracted datetime as the key
    sorted_filenames = sorted(filenames, key=extract_datetime)
    return sorted_filenames
def extract_wrf_date(filename):
    match = re.search(r'dbz_wrfout_(\w+)_(\d{4}-\d{2}-\d{2})_(\d{2})_(\d{2})_(\d{2})', filename)
    if match:
        date_str = f"{match.group(2)} {match.group(3)}:{match.group(4)}:{match.group(5)}"
        return date_str
    else:
        return None
def load_data_extract_dbz_concat(sorted_filenames_wrf_dbz, directory_wrf, target_pressure=598.0):
    # Sort the name list
    name_list = sorted(sorted_filenames_wrf_dbz)
    dataset_list = []
    for item in name_list:
        item = item[4:]  # Adjust the item as per your requirement
        the_file = Dataset(os.path.join(directory_wrf, item))
        print(item)  # Print the name of the dataset being loaded
        dataset_list.append(the_file)
    # Extract the 'dbz' variable for all times
    p_cat = getvar(dataset_list, "dbz", timeidx=ALL_TIMES, method="cat")
    # Extract the bottom_top pressure levels (assuming you have the pressure levels defined)
    bottom_top_levels = getvar(dataset_list, "pressure", timeidx=ALL_TIMES, method="cat")  
    dbz_at_target_pressure = interplevel(p_cat,bottom_top_levels,target_pressure)
    return dbz_at_target_pressure
def add_prefix_to_strings(string_list, prefix="dbz_"):
    print("adding prefixes to strings")
    return [prefix + s for s in string_list]
def read_wrfout_filenames(directory_path,prefix="wrfout"):
    # List to store filenames
    wrfout_filenames = []
    # Iterate through all files in the specified directory
    for filename in os.listdir(directory_path):
        if filename.startswith(prefix):
            wrfout_filenames.append(filename)
    return wrfout_filenames
def select_radar_files_by_date_range(prefix,directory_wrf):
    print("Calculating reflectivity for wrf data and aggregating the files, please wait...")
    os.chdir(directory_wrf)
    filenames_wrf = read_wrfout_filenames(directory_wrf, prefix=prefix)
    filenames_wrf_dbz = add_prefix_to_strings(filenames_wrf)
    sorted_filenames_wrf = sort_wrfout_filenames(filenames_wrf)
    sorted_filenames_wrf_dbz = add_prefix_to_strings(sorted_filenames_wrf)
    return sorted_filenames_wrf_dbz 

#################################################################################################

import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import wrf
import xarray as xr                                                                                                                  
import matplotlib.pyplot as plt
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,cartopy_ylim, latlon_coords,ALL_TIMES)
from datetime import datetime
import re
from wrf import getvar, interplevel


directory_wrf = r'/mnt/Data/geodata/ikiam/curso-wrf/wrfoutput/'  #original tests
prefix='wrfout_d03'

os.chdir(directory_wrf)
sorted_filenames_wrf_dbz = select_radar_files_by_date_range(prefix,directory_wrf)
print(sorted_filenames_wrf_dbz)


#The following function will calculate dBZ for all the event at the specified pressure level

wrf_merged_file=load_data_extract_dbz_concat(sorted_filenames_wrf_dbz,directory_wrf,598.0)
# Assuming wrf_merged_file is your DataArray or Dataset
wrf_merged_file.attrs['projection'] = str(wrf_merged_file.attrs['projection'])
wrf_merged_file.to_netcdf('wrf_merged_file.nc')

wrf_mean = wrf_merged_file.clip(min=0).mean(dim="Time")


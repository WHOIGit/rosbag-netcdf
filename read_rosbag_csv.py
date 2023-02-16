import re

import numpy as np
import pandas as pd
import xarray as xr 

# CSVs returned by bag_csv have slashes in the column names

def regularize_column_names(df, prefix='/'):
    new_col_names = []

    for col_name in df.columns:
        new_col_name = re.sub(prefix, '', col_name)
        new_col_name = re.sub(r'/', '-', new_col_name)
        new_col_names.append(new_col_name)

    return new_col_names

def as_datetime(epoch_time):
    return pd.to_datetime((epoch_time * 10**9).astype(int), utc=True)

def read_bag_csv(path, prefix='/'):
    bag_data = pd.read_csv(path, index_col=0)

    bag_data.columns = regularize_column_names(bag_data, prefix=prefix)
    bag_data.set_index(as_datetime(bag_data.index), inplace=True)
    bag_data.index.name = 'time'
    
    return bag_data

# read CTD data from exported CSV file

ctd_data = read_bag_csv('data/rosbags/ctd.csv', prefix='/ctd/')

# simplify CTD data

ctd_data = ctd_data[['salinity','temperature','pressure','sound_speed']]

# read GPS data from exported CSV file

gps_data = read_bag_csv('data/rosbags/gps_fix.csv', prefix='/gps/fix/')

# simplify gps data

gps_data = gps_data[['latitude','longitude','altitude']]

# interpolate gps data to the ctd timebase

merged = pd.concat([ctd_data, gps_data])

for col in gps_data.columns:
    merged[col] = np.interp(merged.index, gps_data.index, gps_data[col])

merged_dataset = xr.Dataset.from_dataframe(merged)

merged_dataset.to_netcdf('output/gps_ctd.nc')



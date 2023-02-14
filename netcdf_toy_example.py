import xarray as xr
import pandas as pd

import numpy as np

# requirements
# - xarray
# - netcdf4

# generate some random lat/lon data

def random_walk(size, normalize=True):
    data = np.cumsum(np.random.normal(size=size))
    if normalize:
        data = (data - np.min(data)) / np.ptp(data)
    return data

# arbitrary location near MVCO for no reason

center_lat = 41.329336
center_lon = -70.601111

# arbitrary start time

start_time = pd.to_datetime('2023-01-01')

# generate a lat/lon timeseries

n_gps = 20

gps_time = pd.date_range(start_time, periods=n_gps, freq='30s')

lat = random_walk(n_gps) * 0.001 + center_lat 
lon = random_walk(n_gps) * 0.001 + center_lon

# generate random "ctd" data with a different timebase in the same range

n_ctd = np.random.randint(n_gps * 2, n_gps * 3)

end_time = np.max(gps_time)
ctd_time = pd.date_range(start_time, end_time, periods=n_ctd)

# generate random salinity data

salinity_data = random_walk(n_ctd) * 2 + 30

# interpolate gps data onto the ctd timebase

interpolated_lat = np.interp(ctd_time, gps_time, lat)
interpolated_lon = np.interp(ctd_time, gps_time, lon)

# generate NetCDF

# tabular data so use Pandas

df = pd.DataFrame({
    'lat': interpolated_lat,
    'lon': interpolated_lon,
    'salinity': salinity_data
}, index=ctd_time)

df.index.name = 'time'

# create xarray dataset from the tabular data

dataset = xr.Dataset.from_dataframe(df)

# TODO add some CF-compliant metadata attributes

# generate NetCDF

dataset.to_netcdf('out.nc')
from default_settings import settings

settings.camera_numbers = [1,2,3,4,5,6,7]
#settings.camera_numbers = [99]
#settings.camera_numbers = [4]
settings.bin_size = 4
settings.new_flat_field_window = 600
#settings.start = 1576540800  + (10*24*60*60)# 2019 12 17
settings.start = 1531353600 # 2018-07-12_0000
settings.stop = settings.start + (60*60)
settings.netcdf_filename = '2018-07-12.nc'
settings.interval = 2
settings.piggyback = False

from default_settings import settings
import matplotlib.cm as cm
import numpy as np
import matplotlib.animation as animation


import os
from pmc_analysis.lib.tools import periodic_image_finder

n = 1531402200 # 2018-07-12_1330
start = n - (3*60)
stop = start + (7*60)
interval = 2

settings.camera_numbers = [4,5,6,7]
settings.all_filename_lists = {4: [], 5:[], 6:[], 7:[]}
for cam_num in settings.camera_numbers:
    filenames = periodic_image_finder.find_periodic_images_full_fn(cam_num,
                                                                            start_timestamp=start,
                                                                            stop_timestamp=stop,
                                                                            interval=interval)

    settings.all_filename_lists[cam_num] = filenames

#settings.min_x = -100
#settings.max_x = 100
#settings.x_increment = 2000

#settings.min_y = 10
#settings.max_y = 110
#settings.y_increment = 1000

#settings.bin_factor = 8

#settings.min_x = -70
#settings.max_x = -15
#settings.x_increment = 1000

#settings.min_y = 15
#settings.max_y = 70
#settings.y_increment = 1000
 
#settings.min_x = -40
#settings.max_x = -20
#settings.x_increment = 1000

#settings.min_y = 25
#settings.max_y = 45
#settings.y_increment = 1000

#settings.min_x = -70
#settings.max_x = -45
#settings.x_increment = 1000

#settings.min_y = 25
#settings.max_y = 50
#settings.y_increment = 1000

settings.min_x = -45
settings.max_x = -15
settings.x_increment = 1000

settings.min_y = 55
settings.max_y = 85
settings.y_increment = 1000

settings.bin_factor = 2

settings.xvalues = np.linspace(settings.min_x, settings.max_x, num=settings.x_increment)
settings.yvalues = np.linspace(settings.min_y, settings.max_y, num=settings.y_increment)
settings.individual_frames = False
settings.grid = True
settings.grid_spacing = 5

#settings.provided_grip_map = '/data/mounted_filesystems/nas2/resources/grid_mapping_lookup_tables/1000x1000_khi_section.csv'

#settings.color_scheme = cm.Blues_r

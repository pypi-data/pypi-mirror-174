from default_settings import settings
import matplotlib.cm as cm
import numpy as np
import matplotlib.animation as animation


import os
from pmc_analysis.lib.tools import periodic_image_finder

n = 1531402200 # 2018-07-12_1330
start = n - (3*60)
#stop = start + 2
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

settings.min_x = -50
settings.max_x = -50+1.5
settings.x_increment = 200

settings.min_y = 45-1.5
settings.max_y = 45
settings.y_increment = 200

settings.bin_factor = 2

settings.xvalues = np.linspace(settings.min_x, settings.max_x, num=settings.x_increment)
settings.yvalues = np.linspace(settings.min_y, settings.max_y, num=settings.y_increment)

settings.individual_frames = False

settings.grid = True
settings.grid_spacing = .1

#settings.provided_grip_map = '/data/mounted_filesystems/pmc_analysis_output/2019-09-17--19-51-48_grid_map_movie/map_df.csv'

settings.timestamp_in_image = True

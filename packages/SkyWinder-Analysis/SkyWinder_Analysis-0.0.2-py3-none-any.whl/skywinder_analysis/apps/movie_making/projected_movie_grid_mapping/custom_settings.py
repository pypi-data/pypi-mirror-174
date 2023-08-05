from default_settings import settings
import numpy as np
import matplotlib.animation as animation
import matplotlib.cm as cm


import os
from pmc_analysis.lib.tools import periodic_image_finder
n = 1531402200 # 2018-07-12_1330
#n = 1531165800 # 2018-07-09_1250
#n = 1531155000 # 2018-07-09_1650
#start = n + (10*60)
#stop = start + (18*60)
start = n + (3*60) + 40
stop = start + 30
interval = 30
#settings.camera_numbers = [4,5,6,7]
#settings.all_filename_lists = {4: [], 5:[], 6:[], 7:[]}
settings.cam_nums = [4, 5]
settings.all_filename_lists = {4:[], 5:[]}
for cam_num in settings.cam_nums:
    filenames = periodic_image_finder.find_periodic_images_full_fn(cam_num,
                                                                            start_timestamp=start,
                                                                            stop_timestamp=stop,
                                                                            interval=interval)

    settings.all_filename_lists[cam_num] = filenames

settings.min_x = -70
settings.max_x = settings.min_x + 55
settings.x_increment = 5500 

settings.min_y = 30
settings.max_y = settings.min_y + 40
settings.y_increment = 4000

settings.bin_factor = 4

settings.xvalues = np.linspace(settings.min_x, settings.max_x, num=settings.x_increment)
settings.yvalues = np.linspace(settings.min_y, settings.max_y, num=settings.y_increment)
settings.individual_frames = True
settings.grid = True
settings.grid_spacing = 5
settings.piggyback = False

#settings.color_scheme = cm.Blues_r
settings.timestamp_in_image = False

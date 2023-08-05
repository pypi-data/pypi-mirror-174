from default_settings import settings
import numpy as np
import matplotlib.animation as animation
import matplotlib.cm as cm


import os
from pmc_analysis.lib.tools import periodic_image_finder
#n = 1531402200 # 2018-07-12_1330
#start = n - (70*60)
#stop = start + (60*60)
#interval = 10

#n = 1531054800 # 2018-07-08_1300
n = 1531098000 # 2018-07-09_0100
start = n
stop = start + (120*60)
interval = 10

settings.camera_numbers = [4,5,6,7]
settings.all_filename_lists = {4: [], 5:[], 6:[], 7:[]}
for cam_num in settings.camera_numbers:
    filenames = periodic_image_finder.find_periodic_images_full_fn(cam_num,
                                                                            start_timestamp=start,
                                                                            stop_timestamp=stop,
                                                                            interval=interval)

    settings.all_filename_lists[cam_num] = filenames

settings.min_x = -100
settings.max_x = 100
settings.x_increment = 2000

settings.min_y = 10
settings.max_y = 110
settings.y_increment = 1000

settings.bin_factor = 8

settings.xvalues = np.linspace(settings.min_x, settings.max_x, num=settings.x_increment)
settings.yvalues = np.linspace(settings.min_y, settings.max_y, num=settings.y_increment)
settings.individual_frames = True
settings.grid = False
settings.grid_spacing = 5
settings.color_scheme = cm.Greys_r

settings.timestamp_in_image = False

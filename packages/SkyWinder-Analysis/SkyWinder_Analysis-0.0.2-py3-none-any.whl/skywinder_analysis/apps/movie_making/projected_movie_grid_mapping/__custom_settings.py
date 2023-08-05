from default_settings import settings
import numpy as np
import matplotlib.animation as animation


import os
from pmc_analysis.lib.tools import periodic_image_finder
n = 1531402200 # 2018-07-12_1330
start = n
stop = start + 2
interval = 2

settings.cam_nums = [5]
settings.all_filename_lists = {5:[]}
for cam_num in settings.cam_nums:
    filenames = periodic_image_finder.find_periodic_images_full_fn(cam_num,
                                                                            start_timestamp=start,
                                                                            stop_timestamp=stop,
                                                                            interval=interval)

    settings.all_filename_lists[cam_num] = filenames

settings.min_x = -100 + 45
settings.max_x = settings.min_x + (12*5)
settings.x_increment = 500

settings.min_y = 20
settings.max_y = settings.min_y + (18*5)
settings.y_increment = 750

settings.bin_factor = 8

settings.xvalues = np.linspace(settings.min_x, settings.max_x, num=settings.x_increment)
settings.yvalues = np.linspace(settings.min_y, settings.max_y, num=settings.y_increment)
settings.individual_frames = True
settings.grid = True
settings.grid_spacing = 5

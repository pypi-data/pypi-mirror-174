from default_settings import settings
import numpy as np
import matplotlib.animation as animation
import matplotlib.cm as cm


import os
from pmc_analysis.lib.tools import periodic_image_finder
#n = 1531190700 # 2018 7 10 02 45
n = 1531402200 # 2018 7 12 13 30

start = n - (10*60)
stop = n + (10*60)

#start = n
#stop = n + 30 

#start = 1531285200 # 2018-07-11_0500
#stop = start + (60*60)
interval = 30

#settings.camera_numbers = [4,5,6,7]
#settings.all_filename_lists = {4: [], 5:[], 6:[], 7:[]}
settings.cam_nums = [5,6]
settings.all_filename_lists = {5:[], 6:[]}
for cam_num in settings.cam_nums:
    filenames = periodic_image_finder.find_periodic_images_full_fn(cam_num,
                                                                            start_timestamp=start,
                                                                            stop_timestamp=stop,
                                                                            interval=interval)

    settings.all_filename_lists[cam_num] = filenames

settings.min_x = -50
settings.max_x = 50
settings.x_increment = 1000

settings.min_y = 10
settings.max_y = 110
settings.y_increment = 1000

settings.bin_factor = 4

settings.xvalues = np.linspace(settings.min_x, settings.max_x, num=settings.x_increment)
settings.yvalues = np.linspace(settings.min_y, settings.max_y, num=settings.y_increment)
settings.individual_frames = True
settings.grid = True
settings.grid_spacing = 5
#settings.color_scheme = cm.Blues_r

settings.timestamp_in_image = True


settings.m_per_pixel = 100
settings.min_physical_range = 5e3
settings.tick_spacing = 1

settings.individual_frames = True
settings.wavelength_labels = True
settings.filter_freq = False
settings.low_freq_filter = 1/60e3
settings.high_freq_filter = 1/14e3
settings.text_color = 'white'

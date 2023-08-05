from default_settings import settings
import numpy as np
import matplotlib.animation as animation
import datetime, calendar

import os
from pmc_analysis.lib.tools import periodic_image_finder
 
n = 1531402200 # 2018-07-12_1330
start = n + (4*60)
stop = start + (2*60)
interval = 10

settings.camera_numbers = [4,5,6,7]
settings.all_filename_lists = {4: [], 5:[], 6:[], 7:[]}
idxs = []
#for i in np.arange(55, 71, 0.5):
#    idxs.append(int(i*30))
for i in np.arange(55, 71, 1):
    idxs.append(int(i*30))
for cam_num in settings.camera_numbers:
    filenames = periodic_image_finder.find_periodic_images_full_fn(cam_num,
                                                                            start_timestamp=start,
                                                                            stop_timestamp=stop,
                                                                            interval=interval)

    #for idx in idxs:
    #    settings.all_filename_lists[cam_num].append(filenames[idx])
    settings.all_filename_lists[cam_num] = filenames



c4_filenames = []
c5_filenames = []
c6_filenames = []
c7_filenames = []
datetimes = [
#                datetime.datetime(2018, 7, 9, 13, 20),
#                datetime.datetime(2018, 7, 9, 14, 10),
#                datetime.datetime(2018, 7, 9, 17, 2),
#                datetime.datetime(2018, 7, 9, 17, 22),
#                datetime.datetime(2018, 7, 10, 2, 40),
#                datetime.datetime(2018, 7, 11, 3, 30),
#                datetime.datetime(2018, 7, 11, 5, 8),
#                datetime.datetime(2018, 7, 11, 5, 43),
#                datetime.datetime(2018, 7, 11, 8, 10),
#                datetime.datetime(2018, 7, 11, 8, 48),
#                datetime.datetime(2018, 7, 11, 9, 24),
#                datetime.datetime(2018, 7, 11, 23, 10),
                datetime.datetime(2018, 7, 12, 14, 8),
#                datetime.datetime(2018, 7, 13, 13, 32),
#                datetime.datetime(2018, 7, 13, 21, 55),
#                datetime.datetime(2018, 7, 14, 1, 14),
            ]
timestamps = []
for datetime in datetimes:
    timestamps.append(calendar.timegm(datetime.utctimetuple()))

for timestamp in timestamps:
    c4_filenames.append(periodic_image_finder.find_periodic_images_full_fn(4, timestamp, timestamp+2, 2)[0])
    c5_filenames.append(periodic_image_finder.find_periodic_images_full_fn(5, timestamp, timestamp+2, 2)[0])
    c6_filenames.append(periodic_image_finder.find_periodic_images_full_fn(6, timestamp, timestamp+2, 2)[0])
    c7_filenames.append(periodic_image_finder.find_periodic_images_full_fn(7, timestamp, timestamp+2, 2)[0])

settings.all_filename_lists[4] = c4_filenames
settings.all_filename_lists[5] = c5_filenames
settings.all_filename_lists[6] = c6_filenames
settings.all_filename_lists[7] = c7_filenames




settings.min_x = -100
settings.max_x = 100
settings.x_increment = 200

settings.min_y = 0
settings.max_y = 115
settings.y_increment = 100

settings.bin_factor = 8

#settings.min_x = -50
#settings.max_x = 0
#settings.x_increment = 1000
#
#settings.min_y = 25
#settings.max_y = 75
#settings.y_increment = 1000

settings.xvalues = np.linspace(settings.min_x, settings.max_x, num=settings.x_increment)
settings.yvalues = np.linspace(settings.min_y, settings.max_y, num=settings.y_increment)

settings.individual_frames = True

settings.grid = True
settings.grid_spacing = 5

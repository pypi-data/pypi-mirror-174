from default_settings import settings
import numpy as np
import matplotlib.animation as animation
import matplotlib.cm as cm
import os
import glob
import datetime
from pmc_analysis.lib.tools import periodic_image_finder


#n = 1578136740 # 2020 01 04 0619
#start = n
#stop = start + (1*60) 
#interval = 10

fns = glob.glob('/home/bjorn/cips_piggyback_overlap_maps/overlaps/*')
unix_timestamps = []

for fn in fns:
    f = fn.split('/')[-1]
    y=int(f[0:4])
    m=int(f[5:7])
    d=int(f[8:10])
    hr=int(f[11:13])
    mn=int(f[14:16])
    dt = datetime.datetime(y,m,d,hr,mn)
    unix_ts = dt.replace(tzinfo=datetime.timezone.utc).timestamp()
    unix_timestamps.append(unix_ts)

settings.cam_nums = [99]
settings.all_filename_lists = {99: []}
#settings.camera_numbers = [4,5,6,7]
#settings.all_filename_lists = {4: [], 5:[], 6:[], 7:[]}
for cam_num in settings.cam_nums:
    #filenames = periodic_image_finder.find_periodic_images_full_fn(cam_num,
    #                                                                        start_timestamp=start,
    #                                                                        stop_timestamp=stop,
    #                                                                        interval=interval)
    filenames = []
    for unix_ts in unix_timestamps:
        start = unix_ts
        stop = start + (15*60)+1
        interval = 300
        filenames += periodic_image_finder.find_periodic_images_full_fn(99, start, stop, interval)
    settings.all_filename_lists[cam_num] = filenames

settings.min_x = -35
settings.max_x = 30
settings.x_increment = 400

settings.min_y = 30
settings.max_y = 95
settings.y_increment = 400

settings.bin_factor = 8

settings.xvalues = np.linspace(settings.min_x, settings.max_x, num=settings.x_increment)
settings.yvalues = np.linspace(settings.min_y, settings.max_y, num=settings.y_increment)
settings.individual_frames = True
settings.grid = True
settings.grid_spacing = 5
settings.color_scheme = cm.inferno

settings.timestamp_in_image = True

settings.piggyback = True

settings.centerline = 215.33 # Centerline for piggyback solution

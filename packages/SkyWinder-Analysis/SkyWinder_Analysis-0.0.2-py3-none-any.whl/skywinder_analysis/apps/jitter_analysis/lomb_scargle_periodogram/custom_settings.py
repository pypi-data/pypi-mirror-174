from default_settings import settings
import glob
import os
from pmc_analysis.lib.tools import periodic_image_finder
import numpy as np

settings.hot_pixel_dirs = glob.glob('/data/home/bjorn/pmc-turbo/config/camera_data/hot_pixels/*.npy')
settings.image_shape = (3232,4864)

n = 1531402200 - (30*60)# 2018-07-12_1300
hour_sec = 3600
settings.starts = np.arange(-hour_sec*48, hour_sec*24, hour_sec) + n
settings.duration = 120

settings.camera_number = 4
settings.new_flat_field_window = 600

settings.all_filename_lists = []
for start in settings.starts:
    full_fns = []

    fn_list = periodic_image_finder.find_all_images(settings.camera_number,
                                                    start_timestamp=start,
                                                    stop_timestamp=start+settings.duration)
    if settings.camera_number > 4:
        direc = '/data/mounted_filesystems/nas2/c{0}'.format(settings.camera_number)
    else:
        direc = '/data/mounted_filesystems/nas1/c{0}'.format(settings.camera_number)
    for fn in fn_list:
        full_fns.append(os.path.join(direc, fn))


    settings.all_filename_lists.append(full_fns)

settings.pointing_solutions_dir = '/data/mounted_filesystems/nas2/resources/pointing_solutions/c%d_2018-07-12_2330_solution.csv' % settings.camera_number

settings.min_blob_trajectory_length = len(settings.all_filename_lists[0])//2

from default_settings import settings
import matplotlib.animation as animation


import os
from pmc_analysis.lib.tools import periodic_image_finder
n = 1531400400 # 2018-07-12_0900
start = n
end = start + (120*60)
interval = 2

settings.camera_number = 5

filenames = periodic_image_finder.find_periodic_images(settings.camera_number, start, end, interval)

joined_filenames = []
for fn in filenames:
        joined_filenames.append(os.path.join(('/data/mounted_filesystems/nas2/c%d/'%settings.camera_number), fn))
settings.filenames = joined_filenames

settings.flat_field_filenames = settings.filenames[::5]
settings.writer = animation.writers['ffmpeg'](fps=20, codec='mpeg4', bitrate=2**20)
settings.bin_pixels = (4,4)
settings.rotate = False

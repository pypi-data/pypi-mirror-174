from default_settings import settings
import matplotlib.animation as animation


import os
from pmc_analysis.lib.tools import periodic_image_finder
#n = 1531402200 # 2018-07-12_1330
#start = n - (60*60)
#stop = n + (15*60)
#interval = 10

#n = 1531298400 # 2018-07-11_0840
#start = n
#stop = start + (5*60)
#interval = 2

#n = 1531298400 # 2018-07-11_0840
#start = n + (25*60)
#stop = start + (10*60)
#interval = 2

n = 1531288200 # 2018-07-11_0550
start = n-(5*60)
stop = n + (10*60)
interval = 2

settings.camera_number = 3

settings.filenames = periodic_image_finder.find_periodic_images_full_fn(settings.camera_number,
                                                                        start_timestamp=start,
                                                                        stop_timestamp=stop,
                                                                        interval=interval)

settings.flat_field_filenames = settings.filenames[::10]
settings.writer = animation.writers['ffmpeg'](fps=20, codec='mpeg4', bitrate=2**20)
settings.bin_pixels = (4,4)
settings.rotate = True
#settings.section = [0,3232,0,4864]
settings.section = [0,3232,0,(5*4864)//8]

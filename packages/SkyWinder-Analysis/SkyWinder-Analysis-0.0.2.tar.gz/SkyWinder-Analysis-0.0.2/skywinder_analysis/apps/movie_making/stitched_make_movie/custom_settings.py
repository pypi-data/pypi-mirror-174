from default_settings import settings
import matplotlib.animation as animation
import os
from pmc_analysis.lib.tools import periodic_image_finder
import matplotlib.cm as cm
import datetime
import calendar

n = 1531402200 # 2018-07-12_1330
start = n - (3*60)
stop = start + (8*60)
interval = 2 

c4_filenames = periodic_image_finder.find_periodic_images_full_fn(4, start, stop, interval)
settings.all_filenames = [c4_filenames]
settings.cameras = [4]

settings.use_new_flat_field = True
settings.new_flat_field_reflection_window = 600


settings.bin_pixels = (8,8)

#settings.level_region = [4864 // (4 * settings.bin_pixels[0]),
#                         (4864) // (settings.bin_pixels[0]),#(3 * 4864) // (4 * settings.bin_pixels[0]),
#                         0 // settings.bin_pixels[1],
#                         (len(settings.all_filenames) * 3232) // settings.bin_pixels[1]]
# Level full stitched by central part of all cameras
settings.level_region = [3232//(4 * settings.bin_pixels[0]), (3 * 3232)//(4 * settings.bin_pixels[0]), 0//settings.bin_pixels[1], 4864//settings.bin_pixels[1]]
# Level single camera by central part



settings.color_scheme = cm.Blues_r
#settings.fontcolor = 'white'
#settings.crop = [3232//4,3232,4864//4,5*4864//8]
settings.colorscale_by_frame = True
settings.vmin = False
settings.vmax = False

settings.individual_frames = False
#settings.split_video_len = (20*60 // interval)
settings.font_proportion = 1./48.
settings.no_text = False

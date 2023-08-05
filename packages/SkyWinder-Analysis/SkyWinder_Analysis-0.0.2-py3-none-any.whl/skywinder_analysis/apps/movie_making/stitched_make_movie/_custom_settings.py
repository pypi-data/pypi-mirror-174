from default_settings import settings
import matplotlib.animation as animation
import os
from pmc_analysis.lib.tools import periodic_image_finder
import matplotlib.cm as cm
import datetime
import calendar

n = 1531483200 # 2018-07-13_1200
start = n
stop = start + (120*60)
interval = 10

c4_filenames = periodic_image_finder.find_periodic_images_full_fn(4, start, stop, interval)
c5_filenames = periodic_image_finder.find_periodic_images_full_fn(5, start, stop, interval)
c6_filenames = periodic_image_finder.find_periodic_images_full_fn(6, start, stop, interval)
c7_filenames = periodic_image_finder.find_periodic_images_full_fn(7, start, stop, interval)
settings.all_filenames = [c4_filenames, c5_filenames, c6_filenames, c7_filenames]
settings.cameras = [4, 5, 6, 7]

settings.use_new_flat_field = True
settings.new_flat_field_reflection_window = 600


#settings.bin_pixels = (2,2)
settings.bin_pixels = (4,4)

settings.level_region = [4864 // (4 * settings.bin_pixels[0]),
                         (4864) // (settings.bin_pixels[0]),#(3 * 4864) // (4 * settings.bin_pixels[0]),
                         0 // settings.bin_pixels[1],
                         (len(settings.all_filenames) * 3232) // settings.bin_pixels[1]]
# Level full stitched by central part of all cameras



settings.color_scheme = cm.inferno
#settings.color_scheme = cm.Blues_r
#settings.fontcolor = 'white'
#settings.crop = [0,3232,0,(7*4864)//8]
#settings.crop = [0,3*3232//8,4864//8,4864//2]
settings.colorscale_by_frame = True
settings.vmin = False
settings.vmax = False

settings.individual_frames = False
#settings.split_video_len = (20*60 // interval)
settings.font_proportion = 1./16.

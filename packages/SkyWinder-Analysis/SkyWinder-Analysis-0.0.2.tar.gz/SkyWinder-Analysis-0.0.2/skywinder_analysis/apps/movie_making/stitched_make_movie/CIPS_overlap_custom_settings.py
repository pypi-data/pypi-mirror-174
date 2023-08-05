from default_settings import settings
import matplotlib.animation as animation
import os
from pmc_analysis.lib.tools import periodic_image_finder
import matplotlib.cm as cm
import datetime
import calendar

n = 1577754600 # 2019-12-31_0110
settings.output_name = '2019-12-19_0110_v_shapes.mp4'
start = n
stop = start + (10*60)
interval = 4

filenames = periodic_image_finder.find_periodic_images_full_fn(99, start, stop, interval)
settings.all_filenames = [filenames]
settings.cameras = [99]

settings.filenames = periodic_image_finder.find_periodic_images_full_fn(99, start, stop, interval)

#settings.level_region = [3232//(4 * settings.bin_pixels[0]), (3 * 3232)//(4 * settings.bin_pixels[0]), 0//settings.bin_pixels[1], 4864//settings.bin_pixels[1]]
settings.level_region = [0, 4864//settings.bin_pixels[0], 3232//(4*settings.bin_pixels[0]), (3*3232)//(4*settings.bin_pixels[0])]

settings.use_new_flat_field = False
settings.new_flat_field_reflection_window = 600
settings.all_flat_field_filenames = settings.filenames


settings.bin_pixels = (4,4)

#settings.level_region = [4864 // (4 * settings.bin_pixels[0]),
#                         (4864) // (settings.bin_pixels[0]),#(3 * 4864) // (4 * settings.bin_pixels[0]),
#                         0 // settings.bin_pixels[1],
#                         (len(settings.all_filenames) * 3232) // settings.bin_pixels[1]]
# Level full stitched by central part of all cameras



settings.color_scheme = cm.inferno
#settings.fontcolor = 'white'
settings.crop = [3232//4,3232,4864//4,5*4864//8]
settings.colorscale_by_frame = True
settings.vmin = False
settings.vmax = False

settings.individual_frames = True
#settings.split_video_len = (20*60 // interval)
settings.font_proportion = 1./16.
settings.no_text = True

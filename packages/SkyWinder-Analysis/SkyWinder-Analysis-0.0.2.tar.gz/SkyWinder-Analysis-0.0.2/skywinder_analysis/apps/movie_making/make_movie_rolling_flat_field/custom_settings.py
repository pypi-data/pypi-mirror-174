from default_settings import settings
from pmc_analysis.lib.tools import periodic_image_finder
import glob

n = 1578643200 + (9*60*60)
settings.output_name = '2020-01-10_1700.mp4'
start = n
stop = start + (30*60)
interval = 4

settings.bin_pixels = (4, 4)

settings.rolling_flat_field_size = 600 // interval
settings.filenames = periodic_image_finder.find_periodic_images_full_fn(99, start, stop, interval)

settings.level_region = [3232//(4 * settings.bin_pixels[0]), (3 * 3232)//(4 * settings.bin_pixels[0]), 0//settings.bin_pixels[1], 4864//settings.bin_pixels[1]]

#settings.filenames = glob.glob('/data/pmc_turbo_raw_data/c4/2018-07-13/2018*')[::10]
#settings.level_region = [0//settings.bin_pixels[0],3232//settings.bin_pixels[0],(4864//4)//settings.bin_pixels[1],(3*4864//4)//settings.bin_pixels[1]]

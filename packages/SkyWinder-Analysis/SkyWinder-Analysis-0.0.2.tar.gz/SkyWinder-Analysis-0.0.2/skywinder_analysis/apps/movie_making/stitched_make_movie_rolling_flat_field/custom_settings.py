from default_settings import settings
import os
from pmc_analysis.lib.tools import periodic_image_finder
import matplotlib.animation as animation

n = 1531038600 # 2018-07-08_0830
start = n + (3*60*60)
end = start + (16*60*60)
interval = 60

c4_filenames = periodic_image_finder.find_periodic_images(4, start, end, interval)
c5_filenames = periodic_image_finder.find_periodic_images(5, start, end, interval)
c6_filenames = periodic_image_finder.find_periodic_images(6, start, end, interval)
c7_filenames = periodic_image_finder.find_periodic_images(7, start, end, interval)
nas1 = [c5_filenames, c6_filenames, c7_filenames]
nas2 = [c4_filenames]
settings.all_filenames = []
for filenames in nas2:
    joined_filenames = []
    for fn in filenames:
        joined_filenames.append(os.path.join(('/data/mounted_filesystems/nas1/c%d/'%4), fn))
    settings.all_filenames.append(joined_filenames)
for camera_number, filenames in zip([5,6,7],nas1):
    joined_filenames = []
    for fn in filenames:
        joined_filenames.append(os.path.join(('/data/mounted_filesystems/nas2/c%d/'%camera_number), fn))
    settings.all_filenames.append(joined_filenames)

settings.rolling_flat_field_size = 10
settings.writer = animation.writers['ffmpeg'](fps=20, codec='libx264', bitrate=2 ** 20)
settings.bin_pixels = (16,16)
settings.level_region = [4864 // (4 * settings.bin_pixels[0]),
                         (3 * 4864) // (4 * settings.bin_pixels[0]),
                         (3232 * 2) // settings.bin_pixels[1],
                         (3232 * 3) // settings.bin_pixels[1]]
# Level full stitched by central part of camera 6

settings.mean_region = [0 // settings.bin_pixels[0],
                        3232 // settings.bin_pixels[0],
                        4864 // (4 * settings.bin_pixels[1]),
                        (3 * 4864) // (4 * settings.bin_pixels[1])]
# Compare mean of images using central 50%

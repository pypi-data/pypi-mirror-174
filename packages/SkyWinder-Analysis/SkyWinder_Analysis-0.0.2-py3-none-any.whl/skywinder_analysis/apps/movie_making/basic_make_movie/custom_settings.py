from default_settings import settings
import matplotlib.animation as animation
import glob
import os

settings.camera_number = 3

fns = glob.glob('/data/mounted_filesystems/nas2/10_minutes_piggyback/*')
print(fns)

def timestamp(x):
    return x[63:69]

sorted_fns = sorted(fns, key = timestamp)

settings.filenames = sorted_fns

settings.flat_field_filenames = settings.filenames[::10]
settings.writer = animation.writers['ffmpeg'](fps=20, codec='mpeg4', bitrate=2**20)
settings.bin_pixels = (4,4)
settings.rotate = False
#settings.section = [0,3232,0,4864]
#settings.section = [0,3232,0,(5*4864)//8]

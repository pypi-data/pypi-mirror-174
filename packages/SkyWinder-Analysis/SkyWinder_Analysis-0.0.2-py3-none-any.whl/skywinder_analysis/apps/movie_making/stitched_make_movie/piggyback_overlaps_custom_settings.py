from default_settings import settings
import matplotlib.animation as animation
import os
from pmc_analysis.lib.tools import periodic_image_finder
import matplotlib.cm as cm
import datetime
import calendar

overlaps_unix = [1576417200.0, 1576468620.0, 1576473600.0, 1576480020.0, 1576485780.0, 1576491480.0, 1576497180.0, 1576502880.0, 1576559280.0, 1576565760.0, 1576571460.0, 1576577160.0, 1576582860.0, 1576588560.0, 1576594320.0, 1576651440.0, 1576657140.0, 1576680000.0, 1576685700.0, 1576742820.0, 1576748520.0, 1576777080.0, 1576782840.0, 1576834200.0, 1576839960.0, 1576874220.0, 1576925640.0, 1576931340.0, 1576959900.0, 1577022720.0, 1577028480.0, 1577114160.0, 1577119860.0, 1577148420.0, 1577154120.0, 1577205540.0, 1577211240.0, 1577239800.0, 1577245560.0, 1577296980.0, 1577302680.0, 1577331240.0, 1577336460.0, 1577388360.0, 1577394060.0, 1577428320.0, 1577434080.0, 1577485500.0, 1577491200.0, 1577519760.0, 1577525460.0, 1577576880.0, 1577582580.0, 1577611140.0, 1577616840.0, 1577668260.0, 1577674020.0, 1577702580.0, 1577708280.0, 1577759700.0, 1577765400.0, 1577799660.0, 1577851080.0, 1577856120.0, 1577862540.0, 1577885340.0, 1577891100.0, 1577948220.0, 1577976780.0, 1577982480.0, 1578039600.0, 1578045300.0, 1578131040.0, 1578136740.0, 1578165300.0, 1578171000.0, 1578222420.0, 1578228120.0, 1578256680.0, 1578262380.0, 1578313800.0, 1578319560.0, 1578348120.0, 1578353820.0, 1578405240.0, 1578410940.0, 1578439500.0, 1578445200.0, 1578502320.0, 1578508080.0, 1578536640.0, 1578593760.0, 1578599460.0, 1578628020.0, 1578633000.0, 1578685140.0, 1578690840.0, 1578718860.0, 1578725160.0, 1578776580.0, 1578782280.0, 1578810840.0, 1578816540.0, 1578867960.0, 1578873660.0, 1578902220.0, 1578907920.0, 1578959340.0, 1578965100.0, 1578993660.0, 1578999360.0, 1579050780.0, 1579056480.0, 1579085040.0, 1579090740.0, 1579142160.0, 1579147860.0, 1579176420.0, 1579182180.0]

filenames = []
for overlap in overlaps_unix:
    start = overlap
    stop = start + (15*60) 
    interval = 60
    filenames += periodic_image_finder.find_periodic_images_full_fn(99, start, stop, interval)

settings.all_filenames = [filenames]
settings.cameras = [99]

#settings.level_region = [3232//(4 * settings.bin_pixels[0]), (3 * 3232)//(4 * settings.bin_pixels[0]), 0//settings.bin_pixels[1], 4864//settings.bin_pixels[1]]
settings.level_region = [0, 4864//settings.bin_pixels[0], 3232//(4*settings.bin_pixels[0]), (3*3232)//(4*settings.bin_pixels[0])]

settings.use_new_flat_field = True
settings.new_flat_field_reflection_window = 600
settings.all_flat_field_filenames = False


settings.bin_pixels = (8,8)

#settings.level_region = [4864 // (4 * settings.bin_pixels[0]),
#                         (4864) // (settings.bin_pixels[0]),#(3 * 4864) // (4 * settings.bin_pixels[0]),
#                         0 // settings.bin_pixels[1],
#                         (len(settings.all_filenames) * 3232) // settings.bin_pixels[1]]
# Level full stitched by central part of all cameras



settings.color_scheme = cm.inferno
#settings.fontcolor = 'white'
settings.crop = False #[3232//4,3232,4864//4,5*4864//8]
settings.colorscale_by_frame = True
settings.vmin = False
settings.vmax = False

settings.individual_frames = True
#settings.split_video_len = (20*60 // interval)
settings.font_proportion = 1./16.
settings.no_text = False

settings.piggyback = True

settings.rotate = True
settings.rotate_k = -1

from pmc_analysis.lib.tools import blosc_file
from pmc_analysis.lib.image_processing import binning
from pmc_analysis.lib.image_processing import flat_field
import matplotlib.animation as animation
import scipy.stats
from pmc_analysis.lib.pmc_analysis_app import pmc_analysis_app
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from pmc_analysis.lib.image_processing import stitching
import os
import sys
import time
import pandas as pd
from scipy import interpolate
from pmc_analysis.lib.units import coordinate_transforms


class img_container_series():
    def __init__(self, cam_num=0):
        self.cam_num = cam_num
        self.ff = False
        self.imgs = []
        self.fh = False
        self.fw = False


class GridMapMovieApp(pmc_analysis_app.App):
    def project_images(self):
        self.create_output()
        self.logger.info('Creating container classes')
        frames = len(self.settings.all_filename_lists[self.settings.cam_nums[0]])
        ics = {}
        global_index = 0
        for cam_num in self.settings.cam_nums:
            ic = img_container_series(cam_num=cam_num)

            for fn in self.settings.all_filename_lists[cam_num]:
                img = flat_field.get_final_cleaned_image(fn, self.settings.new_flat_field_window)
                img = binning.bucket(img, (self.settings.bin_factor, self.settings.bin_factor))
                ic.imgs.append(img)
            ics[cam_num] = ic

        if not self.settings.provided_grid_map:
            self.logger.info('Building interpolation functions')
            for cam_num in self.settings.cam_nums:
                df = pd.read_csv(
                    os.path.join(self.settings.pointing_directory,
                                 ('c%d_2018-07-12_2330_solution.csv' % cam_num)))
                f_h = interpolate.interp2d(df.az, df.alt, df.h,
                                           kind='cubic', bounds_error=False, fill_value=np.nan)
                f_w = interpolate.interp2d(df.az, df.alt, df.w,
                                           kind='cubic', bounds_error=False, fill_value=np.nan)
                ics[cam_num].fh = f_h
                ics[cam_num].fw = f_w
            self.logger.info('Interpolation function finished')

            def altaz_to_pixel(alt, az, cam_num, verbose=False):
                h = ics[cam_num].fh(az, alt)
                w = ics[cam_num].fw(az, alt)
                try:
                    h = int(np.rint(h))
                    w = int(np.rint(w))
                except ValueError as e:
                    return False
                if verbose:
                    print('H, W:', h, w)
                if h > 3231:
                    return False
                if w > 4863:
                    return False
                if h < 0:
                    return False
                if w < 0:
                    return False
                else:
                    return h, w

            def get_value(x, y, bin_factor=1, verbose=False):
                alt, az = coordinate_transforms.cart_to_altaz(x, y, verbose=verbose)
                for cam_num in self.settings.cam_nums:
                    coords = altaz_to_pixel(alt, az, cam_num, verbose=verbose)
                    if coords == False:
                        continue
                    else:
                        h, w = coords
                        return h // bin_factor, w // bin_factor, cam_num
                return -1, -1, -1

            hs = []
            ws = []
            cams = []
            for i in self.settings.xvalues:
                for j in self.settings.yvalues:
                    h, w, cam = get_value(i, j, bin_factor=self.settings.bin_factor)
                    hs.append(h)
                    ws.append(w)
                    cams.append(cam)

            map_df = pd.DataFrame(data={'h':hs, 'w':ws, 'cam':cams})
            map_df.to_csv(os.path.join(self.out_path, 'map_df.csv'))
        else:
            map_df = pd.read_csv(self.settings.provided_grid_map)

        xmin = min(self.settings.xvalues)
        xmax = max(self.settings.xvalues)
        ymin = min(self.settings.yvalues)
        ymax = max(self.settings.yvalues)

        vmins = []
        vmaxs = []
        #for cam_num in self.settings.cam_nums:
        #    vmin = scipy.stats.scoreatpercentile(
        #        ics[cam_num].imgs[0][self.settings.level_region[0]:self.settings.level_region[1],
        #        self.settings.level_region[2]:self.settings.level_region[3]]
        #        , .01)
        #    vmax = scipy.stats.scoreatpercentile(
        #        ics[cam_num].imgs[0][self.settings.level_region[0]:self.settings.level_region[1],
        #        self.settings.level_region[2]:self.settings.level_region[3]]
        #        , 99.9)
        #    vmins.append(vmin)
        #    vmaxs.append(vmax)

        #vmin = min(vmins)
        #vmax = max(vmaxs)


        imd = np.zeros((len(self.settings.xvalues), len(self.settings.yvalues)))

        fig = plt.figure(frameon=False)
        ax = fig.add_subplot(111)
        im = ax.imshow(imd, cmap=cm.Blues_r,
                       origin='lower', extent=[xmin, xmax, ymax, ymin])
        ax.set_xlabel('x (km)')
        ax.set_ylabel('y (km)')

        ax.xaxis.set_major_locator(plt.MultipleLocator(25))
        ax.xaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.yaxis.set_major_locator(plt.MultipleLocator(25))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(5))
        ax.set_aspect('equal')
        ax.set_axisbelow(True)
        ax.grid(False)
        ax.set_title('start')

        fig = plt.figure(frameon=False)
        ax = fig.add_subplot(111)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        vsize = imd.shape[0] / self.settings.dpi
        hsize = imd.shape[1] / self.settings.dpi
        fig.set_size_inches([hsize, vsize])


        xfig, yfig = fig.get_dpi() * fig.get_size_inches()

        fontsize = yfig / 48
        #txt = ax.text(0.01 * xfig, 0.002 * yfig, 'time:', ha='left', va='top', color='black', fontsize=fontsize)
        start_at = time.time()
        def update_img(index):
            elapsed = time.time() - start_at
            if index:
                time_per_frame = elapsed / index
            else:
                time_per_frame = 1
            sys.stdout.flush()

            def map_image(i, j):
                #do indexing to get cam, h, and w from df
                i = int(i)
                j = int(j) 
                coords = j + (i*len(self.settings.yvalues))
                entry = map_df.iloc[coords]
                if entry.cam == -1:
                    return np.nan
                else:
                    return ics[entry.cam].imgs[index][entry.h][entry.w]

            vector_map_image = np.vectorize(map_image)
            self.logger.info('Writing frame %d' % index)
            stretched_image = np.fromfunction(vector_map_image,
                                              (len(self.settings.xvalues), len(self.settings.yvalues)))
            #stretched_image = np.rot90(stretched_image, k=1)
            if True:
                vmin = np.nanpercentile(stretched_image, .01)
                vmax = np.nanpercentile(stretched_image, 99.99)
                print(vmin, vmax)
            im.set_data(stretched_image)
            im.set_clim(vmin=vmin, vmax=vmax)


            date_string = self.settings.all_filename_lists[self.settings.cam_nums[0]][index].split('/')[-1].split('_')[0]
            time_string = self.settings.all_filename_lists[self.settings.cam_nums[0]][index].split('/')[-1].split('_')[1]
            # Switch from Eastern time to UT
            hour = int(time_string[0:2])
            hour += 4
            hour = hour % 24
            time_string = (date_string + '_' + ('%d' % hour) + ':' + time_string[2:4] + ':' + time_string[4:])
            ax.set_title(time_string)
            #txt.set_text(time_string)

            #fn = 'projected_' + time_string + '.png'
            #fig.savefig(os.path.join(self.out_path, fn), dpi=self.settings.dpi, bbox_inches='tight')
            self.logger.info("\r%d of %d %.1f minutes elapsed, %.1f minutes remaining" % (index, frames, elapsed/60, (frames-index) * time_per_frame / 60))
            if self.settings.individual_frames:
                fig_fn = os.path.join(self.out_path, ('frame_%d_%s.png' % (n, time_string[4:])))
                plt.savefig(fig_fn)
                self.logger.info('Frame saved as %s' % fig_fn)


        if not self.settings.individual_frames:
            ani = animation.FuncAnimation(fig, update_img, frames, interval=500)
            ani_fn = os.path.join(self.out_path, 'movie.mp4')
            ani.save(ani_fn, writer=self.settings.writer, dpi=self.settings.dpi)
            return ani
        else:
            for n in range(frames):
                update_img(n)
            return True





if __name__ == "__main__":
    app = GridMapMovieApp()
    app.project_images()

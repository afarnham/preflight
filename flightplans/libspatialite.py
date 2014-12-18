import os
import tempfile
import shutil
import subprocess

from flightplan import FlightPlan

class SpatialiteFlightPlan(FlightPlan):
    def get_version(self):
        return '4.1.1'

    def get_name(self):
        return 'libspatialite'
   
    def deps(self):
        return ['sqlite3', 'proj4'] #, 'geos']

    def package_options(self):
        return [
            '--disable-freexl',
            #'--with-geosconfig={prefix}/bin/geos-config'.format(prefix=self.prefix),
            '--disable-geos',
            '--disable-examples' # needed if --disable-geos is used
        ]

    def get_resources(self):
        urls = [
            'http://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.1.1.tar.gz'
        ]
        self.download_and_unarchive(urls)
        self.patch()

    def patch(self):
        src_dir = os.path.dirname(os.path.abspath(__file__))
        patch_file = 'libspatialite_' + self.get_version() + '.patch'
        patch_path = os.path.join(src_dir, patch_file)
        with open(patch_path) as f:
            subprocess.call(['patch', '-p1'], stdin=f)

        #subprocess.call(['autoreconf'])
    
        dst_dir = self.working_dir
        srcfile = os.path.join(src_dir, 'libspatialite_updated_files', 'config.guess')
        dstfile = os.path.join(dst_dir, 'config.guess')
        shutil.copyfile(srcfile, dstfile)

        srcfile = os.path.join(src_dir, 'libspatialite_updated_files', 'config.sub')
        dstfile = os.path.join(dst_dir, 'config.sub')
        shutil.copyfile(srcfile, dstfile)

    def cflags(self):
        return '-Wno-error=implicit-function-declaration' #fixes builds for 64-bit devices w/ clang

    def ldflags(self):
        return "-liconv" #-lgeos -lgeos_c -lc++"

FLIGHTPLAN_CLASS = SpatialiteFlightPlan


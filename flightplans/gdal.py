import os
import tempfile
import shutil

from flightplan import FlightPlan

class GDALFlightPlan(FlightPlan):
    def get_version(self):
        return '2.1.1'

    def get_name(self):
        return 'gdal'

    def deps(self):
        return [] # ['proj4', 'sqlite3']

    def package_options(self):
        return [
            '--with-static-proj4={prefix}'.format(prefix=self.prefix),
            '--with-unix-stdio-64=no',
            '--with-sqlite3={prefix}'.format(prefix=self.prefix),
            #'--without-gif', #unable to build on x86_64
            '--with-threads',
            '--with-ogr',
            #'--with-geos',
            '--without-libtool',
            '--with-libz=internal',
            '--with-libtiff=internal',
            '--with-geotiff=internal',
            '--without-gif',
            '--without-pg',
            '--without-grass',
            '--without-libgrass',
            '--without-cfitsio',
            '--without-pcraster',
            '--without-netcdf',
            '--without-png',
            '--without-jpeg',
            '--without-gif',
            '--without-ogdi',
            '--without-fme',
            '--without-hdf4',
            '--without-hdf5',
            '--without-jasper',
            '--without-ecw',
            '--without-kakadu',
            '--without-mrsid',
            '--without-jp2mrsid',
            '--without-bsb',
            '--without-grib',
            '--without-mysql',
            '--without-ingres',
            '--without-xerces',
            '--without-expat',
            '--without-odbc',
            '--without-curl',
            '--without-sqlite3',
            '--without-dwgdirect',
            '--without-panorama',
            '--without-idb',
            '--without-sde',
            '--without-perl',
            '--without-php',
            '--without-ruby',
            '--without-python',
            '--without-ogpython',
            '--with-hide-internal-symbols'
        ]

    def get_resources(self):
        urls = [
        'http://download.osgeo.org/gdal/2.1.1/gdal-2.1.1.tar.gz'
        ]
        self.download_and_unarchive(urls)
        #self.patch()

    def patch(self):
        src_dir = os.path.dirname(os.path.abspath(__file__))
        dst_dir = self.working_dir
        srcfile = os.path.join(src_dir, 'gdal_updated_files', 'config.guess')
        dstfile = os.path.join(dst_dir, 'config.guess')
        shutil.copyfile(srcfile, dstfile)

        srcfile = os.path.join(src_dir, 'gdal_updated_files', 'config.sub')
        dstfile = os.path.join(dst_dir, 'config.sub')
        shutil.copyfile(srcfile, dstfile)

    def cflags(self):
        return '-Wno-error=implicit-function-declaration' #fixes builds for 64-bit devices w/ clang

FLIGHTPLAN_CLASS = GDALFlightPlan

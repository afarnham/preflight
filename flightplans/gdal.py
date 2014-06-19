import os
import tempfile
import shutil

from flightplan import FlightPlan

class GDALFlightPlan(FlightPlan):
    def get_version(self):
        return '1.10.1'

    def get_name(self):
        return 'gdal'
   
    def deps(self):
        return ['proj4', 'sqlite3']

    def package_options(self):
        return [
            '--with-static-proj4={prefix}'.format(prefix=self.prefix),
            '--with-unix-stdio-64=no',
            '--with-sqlite3={prefix}'.format(prefix=self.prefix),
            '--without-gif' #unable to build on x86_64
        ]

    def get_resources(self):
        urls = [
            'http://download.osgeo.org/gdal/1.10.1/gdal-1.10.1.tar.gz'
        ]
        self.download_and_unarchive(urls)
        self.patch()

    def patch(self):
        src_dir = os.path.dirname(os.path.abspath(__file__))
        dst_dir = self.working_dir
        srcfile = os.path.join(src_dir, 'gdal_updated_files', 'config.guess')
        dstfile = os.path.join(dst_dir, 'config.guess')
        shutil.copyfile(srcfile, dstfile)

        srcfile = os.path.join(src_dir, 'gdal_updated_files', 'config.sub')
        dstfile = os.path.join(dst_dir, 'config.sub')
        shutil.copyfile(srcfile, dstfile)
    
FLIGHTPLAN_CLASS = GDALFlightPlan


import os
import tempfile
import shutil

from flightplan import FlightPlan

class GEOSFlightPlan(FlightPlan):
    def get_version(self):
        return '3.4.2'

    def get_name(self):
        return 'geos'
   
    def deps(self):
        return []

    def package_options(self):
        return []

    def get_resources(self):
        urls = [
            'http://download.osgeo.org/geos/geos-3.4.2.tar.bz2'
        ]
        self.download_and_unarchive(urls)
        self.patch()

    def patch(self):
        src_dir = os.path.dirname(os.path.abspath(__file__))
        dst_dir = self.working_dir
        srcfile = os.path.join(src_dir, 'libspatialite_updated_files', 'config.guess')
        dstfile = os.path.join(dst_dir, 'config.guess')
        shutil.copyfile(srcfile, dstfile)

        srcfile = os.path.join(src_dir, 'libspatialite_updated_files', 'config.sub')
        dstfile = os.path.join(dst_dir, 'config.sub')
        shutil.copyfile(srcfile, dstfile)

FLIGHTPLAN_CLASS = GEOSFlightPlan


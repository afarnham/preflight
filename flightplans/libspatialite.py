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
        return ['sqlite3', 'proj4']

    def package_options(self):
        return [
            '--disable-freexl',
            '--disable-geos',
            '--disable-examples', # needed if --disable-geos is used
        ]

    def get_resources(self):
        urls = [
            'http://www.gaia-gis.it/gaia-sins/libspatialite-4.1.1.tar.gz'
        ]
        self.download_and_unarchive(urls)
        self.patch()

    def patch(self):
        patch_file = 'libspatialite_' + self.get_version() + '.patch'
        patch_path = os.path.dirname(os.path.abspath(__file__))
        patch_path = os.path.join(patch_path, patch_file)
        with open(patch_path) as f:
            subprocess.call(['patch', '-p1'], stdin=f)


FLIGHTPLAN_CLASS = SpatialiteFlightPlan


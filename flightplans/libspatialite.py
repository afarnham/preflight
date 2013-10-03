import os
import tempfile
import shutil

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
        ]

    def get_resources(self):
        urls = [
            'http://www.gaia-gis.it/gaia-sins/libspatialite-4.1.1.tar.gz'
        ]
        self.download_and_unarchive(urls)
    
FLIGHTPLAN_CLASS = SpatialiteFlightPlan


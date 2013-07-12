import os
import tempfile
import shutil

from flightplan import FlightPlan

class GDALFlightPlan(FlightPlan):
    def get_version(self):
        return '1.10.0'

    def get_name(self):
        return 'gdal'
   
    def deps(self):
        return ['proj4']

    def package_options(self):
        return [
            '--with-static-proj4={prefix}'.format(prefix=self.prefix),
            '--with-unix-stdio-64=no'
        ]

    def get_resources(self):
        urls = [
            'http://download.osgeo.org/gdal/1.10.0/gdal-1.10.0.tar.gz'
        ]
        self.download_and_unarchive(urls)
    
FLIGHTPLAN_CLASS = GDALFlightPlan


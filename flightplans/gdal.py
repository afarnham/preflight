import os
import tempfile
import shutil
from urlparse import urlparse

from flightplan import FlightPlan

class GDALFlightPlan(FlightPlan):
    def get_version(self):
        return '1.10.0'

    def get_name(self):
        return 'gdal'
    
    def package_options(self):
        return [
            '--disable-shared',
            '--enable-static',
            '--with-unix-stdio-64=no'
        ]

    def get_resources(self):
        urls = [
            'http://download.osgeo.org/gdal/1.10.0/gdal-1.10.0.tar.gz'
        ]
        os.chdir(self.cache)
        for url in urls:
            parsed_url = urlparse(url)
            filename = os.path.split(parsed_url.path)[1]
            full_path = os.path.join(self.cache, filename)
            if not os.path.exists(full_path):
                self.download_url(url)
    
            full_cache_path = os.path.join(self.cache, filename)
            self.unarchive(full_cache_path, self.working_dir)
        os.chdir(self.working_dir)
    
FLIGHTPLAN_CLASS = GDALFlightPlan


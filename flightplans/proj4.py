import os
import tempfile
import shutil
from urlparse import urlparse

from flightplan import FlightPlan

class Proj4FlightPlan(FlightPlan):
    def get_version(self):
        return '4.9.0RC2'

    def get_name(self):
        return 'proj4'
   
    def deps(self):
        return []

    def package_options(self):
        return []

    def get_resources(self):
        urls = [
            'http://download.osgeo.org/proj/proj-4.9.0RC2.tar.gz'
        ]
        self.download_and_unarchive(urls)

FLIGHTPLAN_CLASS = Proj4FlightPlan


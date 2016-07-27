import os
import tempfile
import shutil
from urlparse import urlparse

from flightplan import FlightPlan

class JPEGFlightPlan(FlightPlan):
    def get_version(self):
        return '9b'

    def get_name(self):
        return 'jpeg'

    def deps(self):
        return []

    def package_options(self):
        return []

    def get_resources(self):
        urls = [
        'http://www.ijg.org/files/jpegsrc.v9b.tar.gz'
        ]
        self.download_and_unarchive(urls)

FLIGHTPLAN_CLASS = JPEGFlightPlan

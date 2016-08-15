import os
import tempfile
import shutil
from urlparse import urlparse

from flightplan import FlightPlan

class PNGFlightPlan(FlightPlan):
    def get_version(self):
        return '1.6.23'

    def get_name(self):
        return 'png'

    def deps(self):
        return []

    def package_options(self):
        return [
            '--host=arm-apple-darwin',
            # '--with-zlib-prefix='
            # '--disable-freexl',
            # '--disable-libxml2',
            # #'--with-geosconfig={prefix}/bin/geos-config'.format(prefix=self.prefix),
            # '--disable-geos',
            # '--disable-examples' # needed if --disable-geos is used
        ]

    def get_resources(self):
        urls = [
            'http://downloads.sourceforge.net/project/libpng/libpng16/1.6.23/libpng-1.6.23.tar.gz'
        ]
        self.download_and_unarchive(urls)

    def cppflags(self):
        return '-I{sysroot}/usr/include'.format(sysroot=self.sysroot)

    def ldflags(self):
        return '-lz'
FLIGHTPLAN_CLASS = PNGFlightPlan

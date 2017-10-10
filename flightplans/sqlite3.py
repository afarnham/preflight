import os
import tempfile
import shutil

from flightplan import FlightPlan

class SQLite3FlightPlan(FlightPlan):
    def get_version(self):
        return '3.20.1'

    def get_name(self):
        return 'sqlite3'
   
    def deps(self):
        return []

    def get_make_params(self):
        return ['libsqlite3.la']

    def package_options(self):
        return [
            '--disable-editline'
        ]

    def get_resources(self):
        urls = [
            'https://www.sqlite.org/2017/sqlite-autoconf-3200100.tar.gz'
        ]
        self.download_and_unarchive(urls)
        
    def cflags(self):
    	flags = ['-DSQLITE_SOUNDEX', 
                 '-DSQLITE_ENABLE_RTREE',
                 '-DSQLITE_DEFAULT_MMAP_SIZE=0',
                 '-DSQLITE_ENABLE_FTS4_UNICODE61',
                 '-DSQLITE_ENABLE_FTS3_PARENTHESIS',
                 '-DSQLITE_ENABLE_LOCKING_STYLE=1',
                 '-DSQLITE_OMIT_AUTORESET',
                 '-DSQLITE_OMIT_BUILTIN_TEST',
                 '-DSQLITE_TEMP_STORE=1',
                 '-DSQLITE_THREADSAFE=1',
                 ]
    	return ' '.join(flags)

    def install_package(self):
        '''Override the standard install_package() call because sqlite3 make install tries to build the sqlite3 shell too. 
        The shell uses deprecated calls that fail to compile and cause this script to break'''
        cwd = os.getcwd()
        include_dir = self.prefix + '/include'
        if not os.path.exists(include_dir):
            os.makedirs(include_dir)
        shutil.move(cwd + "/.libs/libsqlite3.a", self.prefix + "/libsqlite3.a")
        shutil.move(cwd + "/sqlite3.h", include_dir + "/sqlite3.h")
        shutil.move(cwd + "/sqlite3ext.h", include_dir + "/sqlite3ext.h")


FLIGHTPLAN_CLASS = SQLite3FlightPlan


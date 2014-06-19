import os
import tempfile
import shutil

from flightplan import FlightPlan

class SQLite3FlightPlan(FlightPlan):
    def get_version(self):
        return '3.8.0.2'

    def get_name(self):
        return 'sqlite3'
   
    def deps(self):
        return []

    def package_options(self):
        return []

    def get_resources(self):
        urls = [
            'http://www.sqlite.org/2013/sqlite-autoconf-3080002.tar.gz'
        ]
        self.download_and_unarchive(urls)
        
    def cflags(self):
    	flags = ['-DSQLITE_SOUNDEX', 
                 '-DSQLITE_ENABLE_FTS4_UNICODE61',
                 '-DSQLITE_ENABLE_FTS3_PARENTHESIS',
                 '-DSQLITE_ENABLE_LOCKING_STYLE=1',
                 '-DSQLITE_OMIT_AUTORESET',
                 '-DSQLITE_OMIT_BUILTIN_TEST',
                 '-DSQLITE_TEMP_STORE=1',
                 '-DSQLITE_THREADSAFE=2',
                 ]
    	return ' '.join(flags)
    
FLIGHTPLAN_CLASS = SQLite3FlightPlan


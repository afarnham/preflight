import subprocess
import os
import tarfile
import shutil
from urlparse import urlparse

class FlightPlan(object):
    def _configure_options(self):
        options = self._default_options()
        package_opts = self.package_options()
        if len(package_opts) > 0:
            options.extend(self.package_options())
        return options

    def _default_options(self):
        arch = self.arch
        if arch == 'arm64':
            arch = 'aarch64'
        default_options = [
            '--prefix={prefix}'.format(prefix=self.prefix),
            '--host={arch}-apple-darwin'.format(arch=arch),
            '--disable-shared',
            '--enable-static'
        ]
        return default_options

    def set_build_info(self, cache, working_directory, arch, platform, prefix):
        self.cache = cache
        self.working_dir = working_directory
        self.arch = arch
        self.platform = platform
        self.prefix = prefix
        
    def get_version(self):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def get_sourcepath(self):
        return self.get_name() + '/' + self.get_version()

    def get_resources(self):
        raise NotImplementedError

    def package_options(self):
        return []

    def clean_package(self):
        subprocess.call(['make', 'clean'])

    def make_package(self):
        subprocess.call(['make', 'install'])

    def build_package(self):
        self.clean_package()
        self.get_resources()
        configure_command = ['./configure']
        opts = self._configure_options()
        if len(opts) > 0:
            configure_command.extend(self._configure_options())
        print ' '.join(configure_command)
        subprocess.check_output(configure_command, stderr=subprocess.STDOUT)
        self.make_package()

    def download_url(self, url):
        print "Downloading", url
        curl_command = ['curl', '-O', '-#', url]
        subprocess.check_call(curl_command)

    def unzip_to_path(input_zipfile, output_path):
        '''
        Utility for unzipping a given file. Not yet implemented.
        '''
        raise NotImplementedError     

    def unarchive(self, input_archive, output_dir):
        tf = tarfile.open(input_archive)
        top_level_dir = tf.firstmember.name
        print "Extracting", top_level_dir
        tf.extractall()
        tf.close()
        shutil.rmtree(output_dir)
        shutil.move(top_level_dir, output_dir)

    def download_and_unarchive(self, urls):
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

    def cflags(self):
        return ''
    
    def cxxflags(self):
        return ''
    
    def ldflags(self):
        return ''
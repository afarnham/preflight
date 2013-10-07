#!/usr/bin/python

import os
import importlib
import sys
import subprocess
import tempfile
import shutil
from urlparse import urlparse

IPHONE_PLATFORM = 'iphoneos'
SIM_PLATFORM = 'iphonesimulator'
DEFAULT_PREFIX_BASE = '~/iOS_lib'

XCODE_4_6_DEFAULTS = {'xcode_version': 4.6,
                      'min_deployment_version': '6.1'}
XCODE_5_0_DEFAULTS = {'xcode_version': 5.0,
                      'min_deployment_version': '7.0'}
DEFAULT_XCODE = XCODE_4_6_DEFAULTS

def min_deployment_version():
    return DEFAULT_XCODE['min_deployment_version']

def architectures(platform):
    return {IPHONE_PLATFORM: ['armv7', 'armv7s'],
            SIM_PLATFORM: ['i386']}[platform]

def get_platforms():
    return [IPHONE_PLATFORM, SIM_PLATFORM]

def append_options(compiler, platform):
    output = compiler
    if platform == SIM_PLATFORM:
        output += ' -mios-simulator-version-min={min_version}'.format(min_version=min_deployment_version())
    return output

def get_cc(platform):
    cc = 'xcrun --sdk {platform} clang'.format(platform=platform)
    cc = append_options(cc, platform)
    return cc

def get_cxx(platform):
    cxx = 'xcrun --sdk {platform} clang++'.format(platform=platform)
    cxx = append_options(cxx, platform)
    return cxx

def get_cflags(arch, platform):
    common_flags = '-arch {arch} -pipe -Os -gdwarf-2 -I{prefix}/include'.format(arch=arch, prefix=get_prefix(arch, platform))
    platform_flags = {
        IPHONE_PLATFORM : '-mthumb',
        SIM_PLATFORM : None
    }

    cflags = common_flags
    if platform_flags[platform] is not None:
        cflags += ' ' + platform_flags[platform]
    return cflags

def get_ldflags(arch, platform):
    #Example sysroot directory: /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS7.0.sdk
    sysroot = ""
    if DEFAULT_XCODE['xcode_version'] == 4.6:
        xcode_path = subprocess.check_output(['xcode-select', '--print-path']).strip()
        sysroot = os.path.join(xcode_path, 'Platforms', platform + '.platform', 'Developer', 'SDKs', '{platform}{version}.sdk'.format(platform=platform, version=min_deployment_version()))
    else:
        sysroot = subprocess.check_output(['xcrun', '--show-sdk-path', '--sdk', platform])
    flags = "-arch {arch} -isysroot {sysroot} -L{prefix}/lib".format(arch=arch,
                                                                     sysroot=sysroot.strip(),
                                                                     platform=platform,
                                                                     prefix=get_prefix(arch, platform))
    return flags

def get_cxxflags(arch, platform):
    return get_cflags(arch, platform)

def get_c_preprocessor():
    return '/usr/bin/clang -E'

def get_cxx_preprocessor():
    return get_c_preprocessor()

def get_user_default_prefix():
    return os.path.expanduser('~/iOS_libs')

def get_prefix(arch, platform):
    path = get_user_default_prefix()
    path_args = {
        'arch' : arch,
        'platform' : platform,
        'min_version' : min_deployment_version()
    }
    prefix_path = os.path.join(path, '{arch}/{platform}.platform/{platform}{min_version}.sdk'.format(**path_args))
    return prefix_path


def set_env(arch, platform):
    CC = get_cc(platform)
    os.environ['CC']=CC

    CFLAGS = get_cflags(arch, platform)
    os.environ['CFLAGS']=CFLAGS

    LDFLAGS = get_ldflags(arch, platform)
    os.environ['LDFLAGS']=LDFLAGS

    CXX = get_cxx(platform)
    os.environ['CXX']=CXX

    CXXFLAGS = get_cxxflags(arch, platform)
    os.environ['CXXFLAGS']=CXXFLAGS

    CPP = get_c_preprocessor()
    os.environ['CPP']=CPP

    CXXCPP = get_cxx_preprocessor()
    os.environ['CXXCPP']=CXXCPP

def chdir_flightbag(flightplan):
    path = os.path.join(os.getcwd(), 'Flightbag', flightplan.get_sourcepath())
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)
    return path

def cache_path():
    cache_path = os.path.expanduser("~/Library/Caches/PreFlight")
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    return cache_path

def build_flightplan(flightplan_name):
    flightplan_module = importlib.import_module('flightplans.{0}'.format(flightplan_name))
    orig_path = os.getcwd()
    flightplan = flightplan_module.FLIGHTPLAN_CLASS()
    working_dir = chdir_flightbag(flightplan)
    cache = cache_path()

    for dep in flightplan.deps():
        build_flightplan(dep)

    print "-----------------------------------------"
    
    for platform in get_platforms():
        for arch in architectures(platform):
            set_env(arch, platform)
            prefix = get_prefix(arch, platform)
            if not os.path.exists(prefix):
                os.makedirs(prefix)
            flightplan.set_build_info(cache, working_dir, arch, platform, get_prefix(arch, platform))
            flightplan.build_package()
    os.chdir(orig_path)

def main():
    if len(sys.argv) >= 3:
        command = sys.argv[1]
        flightplan_name = sys.argv[2]
        if command == 'build':
            build_flightplan(flightplan_name)


if __name__ == '__main__':
    main()
            
    

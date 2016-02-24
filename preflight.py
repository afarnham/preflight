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

XCODE_7_DEFAULTS = {'xcode_version': 7.2,
					'iphone_archs': ['armv7', 'arm64'],
					'sim_archs': ['i386', 'x86_64'],
                    'min_deployment_version': '8.2'}
DEFAULT_XCODE = XCODE_7_DEFAULTS

def min_deployment_version():
    return DEFAULT_XCODE['min_deployment_version']

def architectures(platform):
    return {IPHONE_PLATFORM: DEFAULT_XCODE['iphone_archs'],
            SIM_PLATFORM: DEFAULT_XCODE['sim_archs']}[platform]

def get_platforms():
    return [IPHONE_PLATFORM, SIM_PLATFORM]

def append_options(compiler, arch, platform):
    output = compiler
    if platform == SIM_PLATFORM:
        output += ' -mios-simulator-version-min={min_version}'.format(min_version=min_deployment_version())
    elif platform == IPHONE_PLATFORM and arch == 'arm64':
        output += ' -mios-version-min={version}'.format(version=min_deployment_version())
    return output


def get_sysroot(platform):
    sysroot = subprocess.check_output(['xcrun', '--show-sdk-path', '--sdk', platform])
    return sysroot.strip()

def get_system(platform):
    system = get_sysroot(platform) + '/usr/include'
    return system

def get_cc(arch, platform):
    cc = 'xcrun --sdk {platform} clang'.format(platform=platform)
    cc = append_options(cc, arch, platform)
    return cc

def get_cxx(arch, platform):
    cxx = 'xcrun --sdk {platform} clang++'.format(platform=platform)
    cxx = append_options(cxx, arch, platform)
    return cxx

def get_cflags(arch, platform):
    common_flags = '-arch {arch} -pipe -Os -gdwarf-2 -isysroot {sysroot} -I{prefix}/include -fembed-bitcode'.format(arch=arch,
                                                                                                    prefix=get_prefix(arch, platform),
                                                                                                    sysroot=get_sysroot(platform))
    platform_flags = {
        IPHONE_PLATFORM : None, #'-mthumb',
        SIM_PLATFORM : None
    }

    cflags = common_flags
    if platform_flags[platform] is not None:
        cflags += ' ' + platform_flags[platform]
    return cflags

def get_ldflags(arch, platform):
    #Example sysroot directory: /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS7.0.sdk
    sysroot = ""
#    if DEFAULT_XCODE['xcode_version'] == 4.6:
#        xcode_path = subprocess.check_output(['xcode-select', '--print-path']).strip()
#        sysroot = os.path.join(xcode_path, 'Platforms', platform + '.platform', 'Developer', 'SDKs', '{platform}{version}.sdk'.format(platform=platform, version=min_deployment_version()))
#    else:
    sysroot = subprocess.check_output(['xcrun', '--show-sdk-path', '--sdk', platform])
    flags = "-arch {arch} -isysroot {sysroot} -L{prefix}/lib".format(arch=arch,
                                                                     sysroot=get_sysroot(platform),
                                                                     platform=platform,
                                                                     prefix=get_prefix(arch, platform))
    return flags

def get_cxxflags(arch, platform):
    return get_cflags(arch, platform)

def get_c_preprocessor(platform):
    return subprocess.check_output(['xcrun', '-f', 'clang', '--sdk', platform]).strip() + ' -E' #'/usr/bin/clang -E'

def get_cxx_preprocessor(platform):
    return get_c_preprocessor(platform)

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


def set_env(arch, platform, flightplan):
    CC = get_cc(arch, platform)
    os.environ['CC']=CC

    CFLAGS = get_cflags(arch, platform)
    CFLAGS = ' '.join([CFLAGS, flightplan.cflags()])
    os.environ['CFLAGS']=CFLAGS
    
    LDFLAGS = get_ldflags(arch, platform)
    LDFLAGS = ' '.join([LDFLAGS, flightplan.ldflags()])
    os.environ['LDFLAGS']=LDFLAGS

    CXX = get_cxx(arch, platform)
    os.environ['CXX']=CXX

    CXXFLAGS = get_cxxflags(arch, platform)
    CXXFLAGS = ' '.join([CXXFLAGS, flightplan.cxxflags()])
    os.environ['CXXFLAGS']=CXXFLAGS

    CPP = get_c_preprocessor(platform)
    os.environ['CPP']=CPP

    CXXCPP = get_cxx_preprocessor(platform)
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


def print_env_var(varname, value):
    print varname + '=' + "'" + value + "'"

def print_env(arch, platform):

    CC = get_cc(arch, platform)
    CFLAGS = get_cflags(arch, platform)
    LDFLAGS = get_ldflags(arch, platform)
    CXX = get_cxx(arch, platform)
    CXXFLAGS = get_cxxflags(arch, platform)
    CPP = get_c_preprocessor(platform)
    CXXCPP = get_cxx_preprocessor(platform)
    print_env_var('CC', "$(" + CC + ")")
    print_env_var('CFLAGS', CFLAGS)
    print_env_var('LDFLAGS', LDFLAGS)
    print_env_var('CXX', "$(" + CXX + ")")
    print_env_var('CXXFLAGS', CXXFLAGS)
    print_env_var('CPP', CPP)
    print_env_var('CXXCPP', CXXCPP)
    

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
            set_env(arch, platform, flightplan)
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
        elif command == 'env':
            arch = sys.argv[2]
            platform = sys.argv[3]
            print_env(arch, platform)


if __name__ == '__main__':
    main()
            
    

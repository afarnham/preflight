#!/usr/bin/python

import os

IPHONE_PLATFORM = 'iphoneos'
SIM_PLATFORM = 'iphonesimulator'

def min_deployment_version():
    return '7.0'

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
    flags = "-arch {arch} -isysroot $(xcrun --show-sdk-path --sdk {platform}) -L{prefix}/lib".format(arch=arch, platform=platform, prefix=get_prefix(arch, platform))
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
    return os.path.join(path, '/{arch}/{platform}.platform/{platform}{min_version}.sdk'.format(**path_args))


def set_env(arch, platform):
    print '-----------------------'
    CC = get_cc(platform)
    print 'CC="{0}"'.format(CC)
    
    CFLAGS = get_cflags(arch, platform)
    print 'CFLAGS="{0}"'.format(CFLAGS)

    LDFLAGS = get_ldflags(arch, platform)
    print 'LDFLAGS="{0}"'.format(LDFLAGS)

    CXX = get_cxx(platform)
    print 'CXX="{0}"'.format(CXX)

    CXXFLAGS = get_cxxflags(arch, platform)
    print 'CXXFLAGS="{0}"'.format(CXXFLAGS)

    CPP = get_c_preprocessor()
    print 'CPP="{0}"'.format(CPP)

    CXXCPP = get_cxx_preprocessor()
    print 'CXXCPP='+CXXCPP


def build_lib():
    for platform in get_platforms():
        for arch in architectures(platform):
            set_env(arch, platform)

if __name__ == '__main__':
    build_lib()
            
    

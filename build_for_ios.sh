#!/bin/bash
################################################################################
#
# Copyright (c) 2008-2009 Christopher J. Stawarz
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################



# Disallow undefined variables
set -u


default_gcc_version=4.2
default_iphoneos_version=7.0
default_macos_version=10.8
default_architecture=armv7s
default_prefix="${HOME}/iOS_lib"

#GCC_VERSION="${GCC_VERSION:-$default_gcc_version}"
export IPHONEOS_DEPLOYMENT_TARGET="${IPHONEOS_DEPLOYMENT_TARGET:-$default_iphoneos_version}"
export MACOSX_DEPLOYMENT_TARGET="${MACOSX_DEPLOYMENT_TARGET:-$default_macos_version}"
DEFAULT_ARCHITECTURE="${DEFAULT_ARCHITECTURE:-$default_architecture}"
DEFAULT_PREFIX="${HOME}/iOS_lib"
DEFAULT_PLATFORM="iPhoneOS"

echo Default architecture: $DEFAULT_ARCHITECTURE

usage ()
{
    cat >&2 << EOF
Usage: ${0##*/} [-ht] [-p prefix] [-a arch] target [configure_args]
    -h  Print help message
    -p  Installation prefix (default: \$HOME/Documents/iOS_GDAL...)
    -t  Use 16-bit Thumb instruction set (instead of 32-bit ARM)
    -a  Architecture target for compilation (default: armv7)

The target must be "device" or "simulator".  Any additional arguments
are passed to configure.

The following environment variables affect the build process:

    GCC_VERSION (default: $default_gcc_version)
    IPHONEOS_DEPLOYMENT_TARGET  (default: $default_iphoneos_version)
    MACOSX_DEPLOYMENT_TARGET    (default: $default_macos_version)
    DEFAULT_PREFIX  (default: $default_prefix)
EOF
}

prefix="${DEFAULT_PREFIX}"

echo Prefix: $prefix

while getopts ":hp:a:t" opt; do
    case $opt in
    h  ) usage ; exit 0 ;;
    p  ) prefix="$OPTARG" ;;
    t  ) thumb_opt=thumb ;;
    a  ) DEFAULT_ARCHITECTURE="$OPTARG" ;;
    \? ) usage ; exit 2 ;;
    esac
done
shift $(( $OPTIND - 1 ))

if (( $# < 1 )); then
    usage
    exit 2
fi

target=$1
shift

case $target in

    device )
    arch="${DEFAULT_ARCHITECTURE}"
    platform=iphoneos
    #extra_cflags="-m${thumb_opt:-no-thumb}"
    extra_cflags="-mthumb -DSQLITE_ENABLE_RTREE=1"
    cc="xcrun --sdk ${platform} clang"
    #cxx="xcrun --sdk ${platform} g++"
    cxx="xcrun --sdk ${platform} clang"
    ;;

    simulator )
    arch=i386
    platform=iphonesimulator
    #extra_cflags="-D__IPHONE_OS_VERSION_MIN_REQUIRED=${IPHONEOS_DEPLOYMENT_TARGET%%.*}0000"
    extra_cflags="-DSQLITE_ENABLE_RTREE=1"
    cc="xcrun --sdk ${platform} clang -mios-simulator-version-min=7.0"
    cxx="xcrun --sdk ${platform} clang++ -mios-simulator-version-min=7.0"
    #cxx="/usr/bin/clang++"
    ;;

    * )
    echo No target found!!!
    usage
    exit 2

esac

prefix="${prefix}/${arch}/${platform}.platform/${platform}${IPHONEOS_DEPLOYMENT_TARGET}.sdk"

echo library will be exported to $prefix

export CC="${cc}"
export CFLAGS="-arch ${arch} -pipe -Os -gdwarf-2 ${extra_cflags} -I${prefix}/include"
#export LDFLAGS="-arch ${arch} -isysroot $(xcrun --show-sdk-path --sdk ${platform}) -L${prefix}/lib"
export LDFLAGS="-arch ${arch} -L${prefix}/lib"
export CXX="${cxx}"
export CXXFLAGS="${CFLAGS}"
export CPP="/usr/bin/clang -E"
export CXXCPP="${CPP}"


./configure \
    --prefix="${prefix}" \
    --host="${arch}-apple-darwin" \
    --disable-shared \
    --enable-static \
    --enable-geos=no \
#    --with-unix-stdio-64=no \
#    --with-static-proj4=${prefix} \
#    --with-poppler=${prefix} \
#    --with-spatialite=${prefix} \
    "$@" || exit

make install || exit

cat >&2 << EOF

Build succeeded!  Files were installed in

  $prefix


   EOF

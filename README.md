Preflight
=========

A script for building binaries from UNIX libs for iOS.

Example 
-------

Building libGeoTiff

    ./build_for_ios.sh simulator \
    --with-libtiff=/Users/aaron/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
    --with-libz=/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator6.1.sdk/ \
    --with-proj=/Users/aaron/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
    --with-jpeg=/Users/aaron/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
    --enable-incode-epsg

Options
-------

Valid targets are "simulator" and "device".

Use the option "-a" to change the target architecture (e.g. '-a i386'). Valid values are i386, armv7, armv7s and anything else Apple supports. 

The --with-libz option in the example above shows how to pull in the libz from iOS instead of compiling your own

You should run this script once for each target and archictecture compbination you need. Most people will want device + armv7, device + armv7s, and simulator + i386 

Once all the libraries for each target have been built, put them into a fat lib using lipo.

    lipo i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk/lib/libtiff.a armv7/iPhoneOS.platform/iPhoneOS6.1.sdk/lib/libtiff.a armv7s/iPhoneOS.platform/iPhoneOS6.1.sdk/lib/libtiff.a -output /mylibs/libtiff.a -create


Building spatialite 4.0.0
-------------------------

The script omits FreeXL and GEOS. 

I had to change lines 72-78 of src/gaiaaux/gg_utf8.c and lines 74-80 of src/gaiggeo/gg_shape.c to look like this (i.e. ensure localcharset.h is not used)


    //#if defined(__APPLE__) || defined(__ANDROID__)
    //#include <iconv.h>
    //#include <localcharset.h>
    //#else /* neither Mac OsX nor Android */
    #include <iconv.h>
    #include <langinfo.h>
    //#endif
    
License
-------

Copyright (c) 2013 Raymond Aaron Farnham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

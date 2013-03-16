Builds binaries from UNIX libs for iOS.

Example 

Building GeoTiff

./build_for_ios.sh simulator \
--with-libtiff=/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
--with-libz=/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator6.1.sdk/ \
--with-proj=/Users/aaron/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
--with-jpeg=/Users/aaron/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
--enable-incode-epsg

Options

valid targets are "simulator" and "device"
-a for ARCH (e.g. '-a i386'). Valid values are i386, armv7, armv7s and anything else Apple puts out

The --with-libz example shows how to pull in the libz from iOS instead of compiling your own

You should run this script once for each target + arch compbination you need. For example

device + armv7

device + armv7s

simulator + i386

Once all the libraries for each target have been built, put them into a fat lib using lipo. Example:

lipo i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk/lib/libtiff.a armv7/iPhoneOS.platform/iPhoneOS6.1.sdk/lib/libtiff.a armv7s/iPhoneOS.platform/iPhoneOS6.1.sdk/lib/libtiff.a -output /mylibs/libtiff.a -create

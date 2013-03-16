Builds binaries from UNIX libs for iOS.

Example 

Building GeoTiff

./build_for_ios.sh simulator \
--with-libtiff=/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
--with-libz=/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator6.1.sdk/ \
--with-proj=/Users/aaron/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
--with-jpeg=/Users/aaron/iOS_lib/i386/iPhoneSimulator.platform/iPhoneSimulator6.1.sdk \
--enable-incode-epsg

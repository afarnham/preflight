Preflight
=========

A simple set of Python scripts to automate building static libraries for iOS. This script uses 'flightplans' as configuration items for building a library. 

Usage
-----

    python preflight.py build <flightplan name>
    
Where &lt;flightplan name&gt; is the filename of any python script in the flightplans sub-directory without the '.py' extension.
For example:

    python preflight.py build libspatialite
    
Output currently goes to ~/iOS_libs and is not yet configurable. The library does not create a fat binary for you but it is easy to do:

    lipo -create <path to armv7 lib> <path to armv7s lib> <path to i386 lib> -output myFatBinary.a

Obviously, if you build for other architectures than those above, you can add them as well.

Creating a Flightplan
---------------------

Copy one of the existing ones and use it as a template. The flightplan.py script should also be used as reference since it contains the super class for all flightplans. Each flightplan is just a python script so it should be easily configurable.

More flightplans welcome!

Misc
----

The build directory is preflight/Flightbag. This directory is conveniently ignored by .gitignore.

TODO
----

* The flightplans are currently configured for what I need at my place of work (ForeFlight). Work needs to be done to allow custom configurations with ease.
* Create fat binaries automatically
* Configurable output location
* Package lib + necessary header files

License
-------


Copyright (c) 2013 Raymond A. Farnham

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        
          

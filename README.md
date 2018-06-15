pbkdf2_ctypes.py
================

A pbkdf2 implementation for python using ctypes.

This module implements pbkdf2 for Python using C libraries available on the system (OpenSSL-1+ or CommonCrypto).
    
Note: This module is intended as a plugin replacement of pbkdf2.py (https://github.com/mitsuhiko/python-pbkdf2)
by Armin Ronacher.  There is no need to compile it so it should be usable on any system where OpenSSL 1.0.0+ or CommonCrypto (OS X)
is installed.

Why?
-------

The above stlib based implementation, although excellent, was worsening web2py (http://web2py.com) performance much more than needed
for doing just password hashing. After pondering different options, it was considered that there
would have been a good chance that a system with python shipping hashlib module, could also have OpenSSL installed
for dependency reasons.
The result is that using this module PKCS5 PBKDF2 hashing can be more than 20x times faster than using Armin's stdlib
implementation.

Copyright :copyright: 2013: Michele Comitini
License LGPLv3

CHANGELOG
----------------------
[2018-06-15]
 * v0.99.5: Fix PyPi missing release files.
 
[2013-09-24]
 * v0.99.4: better support for python2.5.  Comply to PATH on Windows.  
   Better OS detection on OS X.

[2013-08-17]
 * v0.99.3: fixed main().  Prepended "_" to internal functions.
 * v0.99.2: added support for python3

[2013-08-16]
 * preparing 0.99.1 to fix problems with pypi

[2013-08-14]
 * added tests.py and prepared for distutils.

[2013-08-08]
 * Update README.md

[2013-08-05]

[2013-07-31]
 * fixed OS X compatibility, should work also on iOS.  Added arg type checks and conversions.

[2013-07-29]
 * added support for common crypto hence hopefully OS X

[2013-07-28]
 * missing () around exceptions
 * pep8
 * now uses ctypes magic to find library
 * added module
 * added module
 * Update README.md
 * Initial commit


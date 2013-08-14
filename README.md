pbkdf2_ctypes.py
=============

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

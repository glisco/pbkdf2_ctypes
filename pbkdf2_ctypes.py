# -*- coding: utf-8 -*-
""" 
    pbkdf2_ctypes
    ~~~~~~

    This module implements pbkdf2 for Python using crypto lib from
    openssl.  
    
    Note: This module is intended as a plugin replacement of pbkdf2.py
    by Armin Ronacher.


    :copyright: Copyright (c) 2013: Michele Comitini <mcm@glisco.it>
    :license: LGPLv3

"""

import ctypes
import hashlib
import platform


try: # check that we have proper OpenSSL on the system.
    if platform.system()=='Windows':
        if platform.architecture()[0] == '64bit':
            crypto = ctypes.CDLL('libeay64.dll')
        else:
            crypto = ctypes.CDLL('libeay32.dll')
    else: # should work on most unix os'.
        crypto = ctypes.CDLL('libcrypto.so')

    PKCS5_PBKDF2_HMAC = crypto.PKCS5_PBKDF2_HMAC

    hashlib_to_crypto_map =  {hashlib.md5: crypto.EVP_md5,
                              hashlib.sha1: crypto.EVP_sha1,
                              hashlib.sha256: crypto.EVP_sha256,
                              hashlib.sha224: crypto.EVP_sha224,
                              hashlib.sha384: crypto.EVP_sha384,
                              hashlib.sha512: crypto.EVP_sha512
    }
except OSError, AttributeError:
    raise ImportError('Cannot find a compatible OpenSSL installation on your system')


def pkcs5_pbkdf2_hmac(data, salt, iterations=1000, keylen=24, hashfunc=None):
    c_pass = ctypes.c_char_p(data)
    c_passlen = ctypes.c_int(len(data))
    c_salt = ctypes.c_char_p(salt)
    c_saltlen = ctypes.c_int(len(salt))
    c_iter = ctypes.c_int(iterations)
    c_keylen = ctypes.c_int(keylen)
    if hashfunc:
        crypto_hashfunc = hashlib_to_crypto_map.get(hashfunc)
        crypto_hashfunc.restype = ctypes.c_void_p
        if crypto_hashfunc is None:
            raise ValueError('Unknown digest' + str(hashfunc))
        c_digest = ctypes.c_void_p(crypto_hashfunc())
    else:
        crypto.EVP_sha1.restype = ctypes.c_void_p
        c_digest = ctypes.c_void_p(crypto.EVP_sha1())
    c_buff = ctypes.create_string_buffer('\000' * keylen)
    err = PKCS5_PBKDF2_HMAC(c_pass, c_passlen,
                            c_salt, c_saltlen,
                            c_iter,
                            c_digest,
                            c_keylen,
                            c_buff)

    if err == 0:
        raise ValueError('wrong parameters')
    return c_buff.raw[:keylen]

def pbkdf2_hex(data, salt, iterations=1000, keylen=24, hashfunc=None):
    return pkcs5_pbkdf2_hmac(data, salt, iterations, keylen, hashfunc).encode('hex')

def pbkdf2_bin(data, salt, iterations=1000, keylen=24, hashfunc=None):
    return pkcs5_pbkdf2_hmac(data, salt, iterations, keylen, hashfunc)


def test():
    failed = []
    def check(data, salt, iterations, keylen, expected):
        rv = pbkdf2_hex(data, salt, iterations, keylen)
        if rv != expected:
            print 'Test failed:'
            print '  Expected:   %s' % expected
            print '  Got:        %s' % rv
            print '  Parameters:'
            print '    data=%s' % data
            print '    salt=%s' % salt
            print '    iterations=%d' % iterations
            print
            failed.append(1)

    # From RFC 6070
    check('password', 'salt', 1, 20,
          '0c60c80f961f0e71f3a9b524af6012062fe037a6')
    check('password', 'salt', 2, 20,
          'ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957')
    check('password', 'salt', 4096, 20,
          '4b007901b765489abead49d926f721d065a429c1')
    check('passwordPASSWORDpassword', 'saltSALTsaltSALTsaltSALTsaltSALTsalt',
          4096, 25, '3d2eec4fe41c849b80c8d83662c0e44a8b291a964cf2f07038')
    check('pass\x00word', 'sa\x00lt', 4096, 16,
          '56fa6aa75548099dcc37d7f03425e0c3')
    # This one is from the RFC but it just takes for ages
    check('password', 'salt', 16777216, 20,
          'eefe3d61cd4da4e4e9945b3d6ba2158c2634e984')
    # From Crypt-PBKDF2
    check('password', 'ATHENA.MIT.EDUraeburn', 1, 16,
          'cdedb5281bb2f801565a1122b2563515')
    check('password', 'ATHENA.MIT.EDUraeburn', 1, 32,
          'cdedb5281bb2f801565a1122b25635150ad1f7a04bb9f3a333ecc0e2e1f70837')
    check('password', 'ATHENA.MIT.EDUraeburn', 2, 16,
          '01dbee7f4a9e243e988b62c73cda935d')
    check('password', 'ATHENA.MIT.EDUraeburn', 2, 32,
          '01dbee7f4a9e243e988b62c73cda935da05378b93244ec8f48a99e61ad799d86')
    check('password', 'ATHENA.MIT.EDUraeburn', 1200, 32,
          '5c08eb61fdf71e4e4ec3cf6ba1f5512ba7e52ddbc5e5142f708a31e2e62b1e13')
    check('X' * 64, 'pass phrase equals block size', 1200, 32,
          '139c30c0966bc32ba55fdbf212530ac9c5ec59f1a452f5cc9ad940fea0598ed1')
    check('X' * 65, 'pass phrase exceeds block size', 1200, 32,
          '9ccad6d468770cd51b10e6a68721be611a8b4d282601db3b36be9246915ec82a')

    raise SystemExit(bool(failed))


if __name__ == '__main__':
    crypto.SSLeay_version.restype = ctypes.c_char_p
    print crypto.SSLeay_version(0)
    for h in hashlib_to_crypto_map:
        pkcs5_pbkdf2_hmac('secret' * 11, 'salt', hashfunc=h)
    test()

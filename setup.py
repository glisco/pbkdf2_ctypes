import os
from setuptools import setup
from pbkdf2_ctypes import __version__ as VERSION

readme = open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r').read()

setup(
    name='pbkdf2-ctypes',
    author='Michele Comitini',
    author_email='mcm@glisco.it',
    version=VERSION,
    url='https://github.com/michele-comitini/pbkdf2_ctypes',
    download_url='https://github.com/michele-comitini/pbkdf2_ctypes/archive/' + VERSION + '.zip',
    py_modules=['pbkdf2_ctypes'],
    description='Very fast implementation of pbkdf2.',
    long_description=readme,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Topic :: Security :: Cryptography',
    ]
)

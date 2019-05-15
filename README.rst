=============
cZipDecrypter
=============
Drip-in replacement of zipfile._ZipDecrypter for python 3.7+

Required:

- Python 3.7 (zipfile._ZipDecrypter has a different interface in python 3.6).
- Cython (only used for building).

Usage::

  import zipfile
  import czipdecrypter
  zipfile._ZipDecrypter = czipdecrypter._ZipDecrypter

from os import urandom
from zipfile import _ZipDecrypter

from czipdecrypter import _ZipDecrypter as C_ZipDecrypter

datalen=2**10
keylen=2**10

if __name__=='__main__':

    data=urandom(datalen)
    key=urandom(keylen)
    assert len(data)==datalen and len(key)==keylen

    func=_ZipDecrypter(key)
    out0=func(data[:12])
    out0+=func(data[12:])

    func=C_ZipDecrypter(key)
    out1=func(data[:12])
    out1+=func(data[12:])

    print('correct' if out0==out1 else 'wrong')

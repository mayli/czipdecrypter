from functools import partial
from os import urandom
from zipfile import _ZipDecrypter

from czipdecrypter import _ZipDecrypter as C_ZipDecrypter

class Timer:
    from time import perf_counter_ns
    def __init__(self,name='',printer=None):
        if not callable(printer):
            raise TypeError('printer is not callable')
        self.printer=printer
        self.name=name
        self.start=0

    def __enter__(self):
        self.start=self.perf_counter_ns()
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        self.end=self.perf_counter_ns()
        self.printer(self.name,self.end-self.start)

def printer(name,duration,result={}):
    if name not in result:
        result[name]=[]
    result[name].append(duration)

datalen=2**22
keylen=2**4
multiple=16

if __name__=='__main__':

    data=urandom(datalen)
    bigdata=urandom(datalen*multiple)
    key=urandom(keylen)
    assert len(data)==datalen
    assert len(bigdata)==datalen*multiple
    assert len(key)==keylen

    rs={}
    _printer=partial(printer,result=rs)
    # initialize crctable
    _ZipDecrypter(b'a')(b'b')

    for n in range(3):
        func=_ZipDecrypter(key)
        with Timer(name='_ZipDecrypter',printer=_printer):
            func(data)

    for n in range(5):
        func=C_ZipDecrypter(key)
        with Timer(name='C_ZipDecrypter',printer=_printer):
            func(bigdata)

    pn='_ZipDecrypter'
    cn='C_ZipDecrypter'
    pavg=sum(rs[pn])/len(rs[pn])
    cavg=sum(rs[cn])/len(rs[cn])
    print('pref: {}/{} {}'.format(cn,pn,pavg*multiple/cavg))

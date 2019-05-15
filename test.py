from functools import partial
from random import randrange
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

if __name__=='__main__':

    data=bytes(bytearray(randrange(256) for n in range(2**24)))
    key=bytes(bytearray(randrange(256) for n in range(2**10)))

    rs={}
    _printer=partial(printer,result=rs)

    for n in range(5):
        with Timer(name='_ZipDecrypter',printer=_printer):
            func=_ZipDecrypter(key)
            out0=func(data[:12])
            out0+=func(data[12:])

        with Timer(name='C_ZipDecrypter',printer=_printer):
            func=C_ZipDecrypter(key)
            out1=func(data[:12])
            out1+=func(data[12:])

    print('correct' if out0==out1 else 'wrong')
    pn='_ZipDecrypter'
    cn='C_ZipDecrypter'
    pavg=sum(rs[pn])/len(rs[pn])
    cavg=sum(rs[cn])/len(rs[cn])
    print('pref: {}/{} {}'.format(cn,pn,pavg/cavg))

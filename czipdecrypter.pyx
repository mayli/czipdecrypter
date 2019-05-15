# cython: language_level=3
# cython: boundscheck=False
# cython: cdivision=True

cdef extern from 'cfunc.c':
    unsigned int crc32(unsigned int ch, unsigned int crc)
    void update_keys(unsigned int c, unsigned int *k)
    unsigned int decrypte(unsigned int c, unsigned int k2)

cdef class _ZipDecrypter:
    cdef unsigned int ks[3]

    def __cinit__(self, bytes pwd):
        cdef unsigned int p
        self.ks[0] = 0x12345678
        self.ks[1] = 0x23456789
        self.ks[2] = 0x34567890

        for p in pwd:
            update_keys(p, self.ks)

    cpdef unsigned int dec(self, unsigned int c):
        c = decrypte(c, self.ks[2])
        update_keys(c, self.ks)
        return c

    def __call__(self, bytes data):
        cdef unsigned int c
        result = bytearray(map(self.dec, data))
        return bytes(result)


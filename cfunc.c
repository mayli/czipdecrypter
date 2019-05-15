#include "crctable.h"

static unsigned int crc32(unsigned int ch,unsigned int crc){
  return (crc >> 8) ^ crctable[(crc ^ ch) & 0xFF];
}

static void update_keys(unsigned int c,unsigned int *k){
  k[0] = crc32(c, k[0]);
  k[1] = (k[1] + (k[0] & 0xFF)) & 0xFFFFFFFF;
  k[1] = (k[1] * 0x8088405 + 1) & 0xFFFFFFFF;
  k[2] = crc32(k[1] >> 24, k[2]);
}

static unsigned int decrypte(unsigned int c,unsigned int k2){
  unsigned int k = k2 | 2;
  return c ^ ((k * (k ^ 1)) >> 8) & 0xFF;
}

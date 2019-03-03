#!/usr/bin/env python3

# Python 3 code that will read, decompress, and then recompress the UE4 game
# save file that Astroneer uses.
#
# Though I wrote this for tinkering with Astroneer games saves, it's probably
# generic to the Unreal Engine 4 compressed saved game format.

import zlib
import sys

print()
filename = sys.argv[1]
with open(filename, 'rb') as compressed:
    header1 = compressed.read(16)
    print("Header: "+''.join('{:02X} '.format(x) for x in header1))
    data_compressed1 = compressed.read()
    data_decompressed1 = zlib.decompress(data_compressed1)
    sz_in  = len(data_compressed1)
    sz_out = len(data_decompressed1)
    with open(filename + '-raw', 'wb') as inflated:
        inflated.write(data_decompressed1)
    print("Inflated from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(sz_in, sz_in, sz_out, sz_out))

with open(filename + '-z', 'wb') as deflated:
    data_compressed2 = bytearray()
    compress = zlib.compressobj(
        6, # Compression level
        zlib.DEFLATED, # default
        (4+8), # Window size
        zlib.DEF_MEM_LEVEL, # default
        0 # Z_DEFAULT_STRATEGY
    )
    #compress = zlib.compressobj()
    data_compressed2 += compress.compress(data_decompressed1)
    data_compressed2 += compress.flush()
    deflated.write(header1)
    deflated.write(data_compressed2)
    sz_in  = len(data_decompressed1)
    sz_out = len(data_compressed2)
    print("Deflated from {:d} (0x{:0x}) to {:d} (0x{:0x}) bytes".format(sz_in,sz_in,sz_out,sz_out))

with open(filename + '-z', 'rb') as compressed:
    header2 = compressed.read(16)
    data_decompressed2 = zlib.decompress(compressed.read())

print()
if data_compressed1 == data_compressed2:
    print("Compressed data matches!")
else:
    print("Compressed data differs (but that may be ok)")

if data_decompressed1 == data_decompressed2:
    print("Decompressed data matches!")
else:
    print("Decompressed data differs (NOT GOOD)")
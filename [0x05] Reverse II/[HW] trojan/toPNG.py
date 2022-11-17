import os
import io
import PIL.Image as Image

from array import array

def readimage(path):
    with open(path, "rb") as f:
        return f.read()

bytes1 = readimage('./c1.bin')
bytes2 = readimage('./c2.bin')
bytes3 = readimage('./c3.bin')
_bytes = bytes1 + bytes2 + bytes3
# print( bytes1 )
# print( bytes2 )
# print( bytes3 )
# print( _bytes )
s = b'0vCh8RrvqkrbxN9Q7Ydx\x00'
a = b''
# print( len( s ) )
for i in range( len( _bytes ) ):
    # print( ( _bytes[i] ^ s[ i % 21 ] ).to_bytes( 1, 'big' ) )
    a += ( _bytes[i] ^ s[ i % 21 ] ).to_bytes( 1, 'big' )
    # print( a )
with open( 'decrypt', "wb" ) as f:
    f.write( a )
# print( len(a), len( _bytes ) )

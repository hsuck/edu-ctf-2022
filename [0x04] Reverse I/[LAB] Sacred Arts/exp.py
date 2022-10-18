from Crypto.Util.number import long_to_bytes

arr = [ 0x8d909984b8beb3ba, 0x8d9a929e98d1928b, 0xd0888bd192909cd2, 0x8c9dc08f978fd1bd, 0xd9c7c7cccdcbc292, 0xc8cfc7cec2be918d, 0xffffffffffff82cf ]

flag = b''
for a in arr:
    b = int( bin( ( 0xffffffffffffffff & ~a ) + 1 ).replace( '0b', '' ), 2 )
    print( b )
    flag += long_to_bytes( b )[::-1]

print( flag )

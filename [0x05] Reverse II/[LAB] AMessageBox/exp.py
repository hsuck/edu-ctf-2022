a = [ 0xb5, 0xe5, 0x8d, 0xbd, 0x5c, 0x46, 0x36, 0x4e, 0x4e, 0x1e, 0x0e, 0x26, 0xa4,
      0x1e, 0x0e, 0x4e, 0x46, 0x06, 0x16, 0xac, 0xb4, 0x3e, 0x4e, 0x16, 0x94, 0x3e,
      0x94, 0x8c, 0x94, 0x8c, 0x9c, 0x4e, 0xa4, 0x8c, 0x2e, 0x46, 0x8c, 0x6c ]

INT_BITS = 8

def rightRotate(n, d):
    # In n>>d, first d bits are 0.
    # To put last 3 bits of at
    # first, do bitwise or of n>>d
    # with n <<(INT_BITS - d)
    return (n >> d)|(n << (INT_BITS - d)) & 0xFF

print( len( a ) )

for i in range( len( a ) ):
    a[i] ^= 0x87
    a[i] = rightRotate( a[i], 3 )
    a[i] = chr( a[i] )
    print( a[i], end='' )

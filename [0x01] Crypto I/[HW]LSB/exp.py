from Crypto.Util.number import *
from pwn import *
from sage.all import *

p = remote( 'edu-ctf.zoolab.org', 10102 )

n = int( p.recvline().decode().strip() )
e = int( p.recvline().decode().strip() )
enc = int( p.recvline().decode().strip() )
print( n, e, enc )

inv_3 = inverse( 3, n )
i = 0
b = 0
pt = 0
while True:
    oracle = ( pow( inv_3, e * i, n ) * enc ) % n
    p.sendline( str( oracle ).encode() )
    r = int( p.recvline().decode().strip() )
    x_i = ( r - ( inv_3 * b ) % n ) % 3

    b = ( inv_3 * b + x_i ) % n
    pt += x_i * ( 3 ** i )
    print( r, x_i, i, pt )

    i += 1

    m = long_to_bytes( pt )
    if b'flag{' in m or b'FLAG{' in m:
        print( m )
        break

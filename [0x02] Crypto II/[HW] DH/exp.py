from pwn import *
from sage.all import *
from Crypto.Util.number import long_to_bytes

enc = 0
while True:
    r = remote( 'edu-ctf.zoolab.org', 10104 )
    p = int( r.recvline().strip() )
    print( 'p=', p )

    if Mod( p - 1, p ).is_square():
        g = Mod( p - 1, p ).sqrt()
        print( 'g=', g )
    else:
        r.close()
        continue

    r.sendline( str( g ).encode() )
    ret = r.recvline().strip()
    if b'Bad :(' in ret:
        r.close()
        continue

    enc = int( ret )
    print( 'enc=', enc )
    break

flag = b''
while True:
    flag = long_to_bytes( int( enc ) )
    if b'flag{' in flag or b'FLAG{' in flag:
        print( flag )
        break
    else:
        enc = enc * g % p

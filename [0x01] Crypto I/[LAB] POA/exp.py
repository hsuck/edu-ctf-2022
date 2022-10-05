from pwn import *

p = remote( 'edu-ctf.zoolab.org', 10101 )
ct = p.readline()[:-1].decode()
ct = bytes.fromhex( ct )
pt = b''
num_blocks = len( ct ) // 16
for block in range( 3, num_blocks ):
    block_pt = b''
    block_ct = ct[ block * 16: ( block + 1 ) * 16 ]
    prev_ct = ct[ ( block - 1 ) * 16: block * 16 ]
    for idx in range( 15, -1, -1 ):
        postfix = bytes([ i ^ j for i, j in zip( block_pt, prev_ct[ idx + 1:] ) ])
        prefix = prev_ct[:idx]
        for i in range( 128, 256 ):
            now = prefix + bytes([ i ^ prev_ct[idx] ]) + postfix + block_ct
            p.sendline( now.hex().encode('ascii') )
            res = p.recvline()
            if res == b'Well received :)\n':
                block_pt = bytes([ i ^ 0x80 ]) + block_pt
                print( block_pt )
                break
        else:
            block_pt = bytes([0x80]) + block_pt

    pt += block_pt

print( pt )


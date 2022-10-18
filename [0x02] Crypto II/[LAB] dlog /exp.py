from pwn import *

p = 143934749405770267808039109533241671783161568136679499142376907171125336784176335731782823029409453622696871327278373730914810500964540833790836471525295291332255885782612535793955727295077649715977839675098393245636668277194569964284391085500147264756136769461365057766454689540925417898489465044267493955801
b = 67

r = remote( 'edu-ctf.zoolab.org', 10103 )

r.readuntil(b'give me a prime')
r.sendline( str(p).encode() )
r.readuntil(b'give me a number')
r.sendline( str(b).encode() )

r.readuntil(b'The hint about my secret:')
ct = int( r.recvline().strip() )

print( ct )

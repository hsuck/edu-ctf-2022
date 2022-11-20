from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'
p = remote( 'edu-ctf.zoolab.org', 10006 )
#p = process('./chal')

p.recvline()

size = []
for i in range(7):
    tmp = p.recvline()
    size.append( int( tmp[-7:-3], 16 ) )
print( size )
order = []
for i in range(7):
    tmp = p.recvline()
    order.insert( 0, tmp[-4] )
print( order )

tcache_0x30 = ''
tcache_0x40 = ''
for i in range( len( order ) ):
    if 0x18 < size[ int( order[i] - ord('A') ) ] <= 0x28:
        tcache_0x30 += chr( order[i] ) + ' --> '
    elif 0x28 < size[ int( order[i] - ord('A') ) ]:
        tcache_0x40 += chr( order[i] ) + ' --> '

tcache_0x30 += 'NULL'
tcache_0x40 += 'NULL'
print( tcache_0x30, tcache_0x40 )
p.recvuntil('?\n> ')
p.sendline( tcache_0x30 )
p.recvuntil('?\n> ')
p.sendline( tcache_0x40 )
p.recvuntil('----------- ** address chall ** -----------\n')

tmp = p.recvline()
_from = tmp[8]
addr = tmp[ 13:13+14 ]
print( chr(_from), addr )

tmp = p.recvline()
to = tmp[0]
print( chr(to) )
p.recvuntil('> ')

to_addr = int( addr, 16 )
for i in range( _from - ord('A'), to - ord('A') ):
    tmp = size[i] - 0x8;
    if tmp % 0x10:
        tmp = ( tmp & ~0xf ) + 0x20;
    else:
        tmp += 0x10;

    to_addr += tmp

print( hex( to_addr ) )
p.sendline( hex( to_addr ) )
p.recvuntil('----------- ** index chall ** -----------\n')

size_2 = 0
for i in range(2):
    tmp = p.recvline()
    size_2 = int( tmp[-7:-3], 16 )
print( size_2 )

p.recvuntil('[')
tmp = p.recvuntil(']')
tmp = tmp.replace( b']', b'' )
print( tmp )
idx = int( tmp )
print( idx )

idx += ( size_2 + 0x10 ) // 0x8
print( idx )

p.recvuntil('> ')
p.sendline( str( idx ) )

p.recvuntil('----------- ** tcache fd chall ** -----------\n')
p.recvline()
p.recvuntil('assert( Y == ')
addr = p.recvuntil(' ')
addr = int( addr.lstrip(b' '), 16 )
print( hex( addr ) )

p.recvuntil('> ')
p.sendline( hex( addr - size_2 - 0x10 ) )

p.recvuntil('assert( Y == ')
addr = p.recvuntil(' ')
addr = int( addr.lstrip(b' '), 16 )
print( hex( addr ) )

p.recvuntil('> ')
p.sendline( hex( addr - size_2 - 0x10 - 0x10 ) )

p.recvall()
#p.interactive()

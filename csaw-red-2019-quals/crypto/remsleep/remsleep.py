from pwn import *
import functools
from Crypto.Cipher import ChaCha20

def xor(a, b):
    return ''.join(chr(ord(x) ^ ord(y)) for x,y in zip(a, b))

def decode(ciphertext, pieces):
    key = functools.reduce(xor, pieces)
    cipher = ChaCha20.new(key=key, nonce=pieces[0][:8])
    return cipher.decrypt(ciphertext)

r = remote("crypto.chal.csaw.io", 1001)

r.recv()
r.sendline("1")

r.recv()
r.sendline("A" * 32)

r.recvuntil("Here's the flag! ")
ciphertext = r.recv().strip().decode("hex")

print(decode(ciphertext, ["A" * 32]))

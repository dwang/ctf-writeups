import base64
import io
from PIL import Image
from pwn import *
from pyzbar import pyzbar

r = remote("chal.pctf.competitivecyber.club", 7070)

r.recvuntil("====================================================================================================\n")

with io.BytesIO() as flag:
  while True:
    response = r.recv()

    if b"That's enough for now..." in response:
      break

    decoded = base64.b64decode(response)

    data = pyzbar.decode(Image.open(io.BytesIO(decoded)))[0].data
    flag.write(base64.b64decode(data.strip()))
    r.sendline(data)

  print(pyzbar.decode(Image.open(flag))[0].data)

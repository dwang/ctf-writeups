import requests

s = requests.Session()

headers = {"Authorization": "secret"}

s.get("http://secretus.insomnihack.ch/secret", headers=headers)
r = s.get("http://secretus.insomnihack.ch/debug/", headers=headers)
print(r.text)

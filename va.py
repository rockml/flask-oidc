import json
import requests as req

tokenfile = open("accesstoken.txt", "r")
token = tokenfile.read()
tokenfile.close()

headers = {"Authorization": "Bearer {}".format(token)}

res = req.get("https://dev-api.va.gov/oauth2/userinfo", headers=headers)
print(res)
print(res.json())

res = req.get("https://dev-api.vets.gov/services/argonaut/v0/Patient/1012829910V765228", headers=headers)
print(res)
res.json()

res = req.get("https://dev-api.vets.gov/services/veteran_verification/v0/status", headers=headers)
print(res)
res.json()


import requests

url = "http://localhost:9712/user/login"

token_data = {
    "token": "eyJhbGciOiasdfsdfsdzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDAxNzY2ODIsInVzZXIiOiJBZHJpYW4iLCJwc3ciOiIxMjMyNDMyNDIzNCJ9.NeG0XlgyaR2UlL3WlOOdlAGIPL3p30K0R5DhDM_246U"
}

credentials_data = {
    "user": "Juan",
    "psw": "09eu0wdod0aud"
}

response = requests.post(url, json=credentials_data)

print(response.json())

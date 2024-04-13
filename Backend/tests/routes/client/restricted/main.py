import requests

url = "http://localhost:8000/app/api/v1/client/restricted/status"

data = {
    "token_id": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjp7ImlkIjoiNjYxYTRkMTIwYjAyNTMyMDc0MmRmZTA5In0sImV4cCI6MTcxNTYxNTg4Mn0.w06WV7I6dtjogrwne_HTXQX9jzzVpFbiHOhKpt-z6rI",
    "token_data": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjp7ImVtYWlsIjoiYWRyaWFuZWxjYXBvQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiZnVja195b3UifSwiZXhwIjoxNzE1NjI5MDY4fQ.Rm_XaqodTz-MsibE_SzAjZN6zyhMDjmBD1rVbxtWj9g"
}

response = requests.post(url, json=data)

print("Código de estado de la respuesta:", response.status_code)

data = response.json()

print("Contenido de la respuesta:")
print(data)

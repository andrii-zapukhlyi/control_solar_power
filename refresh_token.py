import requests, time, hmac, hashlib, json

### Signature algorithm
def generate_signature(client_id, client_secret, current_time, url):
    http_method = "GET"
    content_sha256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    string_to_sign = f"{client_id}{current_time}{http_method}\n{content_sha256}\n\n{url}"
    signature = hmac.new(client_secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest().upper()
    return signature

### Read token.json file
with open("token.json", "r") as file:
    token_file = json.load(file)

refresh_token = token_file["result"]["refresh_token"]                       ### Get refresh token from the file token.json

"""
REPLACE THE DATA BELOW
"""

client_id = "client_id"                                                     ### Replace with your Cliend ID obtained in the section Authorization in Smart Home cloud project
client_secret = "client_secret"                                             ### Replace with your Client Secret obtained in the section Authorization in Smart Home cloud project

timestamp = str(int(time.time() * 1000))                                    ### UTC 13-digits timestamp used to generate signature
url = f"/v1.0/token/{refresh_token}"                                        ### URL for GET request to get the access token
signature = generate_signature(client_id, client_secret, timestamp, url)    ### Generate signature for the request

headers = {
    "client_id": client_id,
    "sign": signature,
    "t": timestamp,
    "sign_method": "HMAC-SHA256"
}

try:
    response = requests.get(f"https://openapi.tuyaeu.com{url}", headers=headers)
except Exception as e:
    print(e)

### Refresh the token.json file
with open("token.json", 'w') as f:
    json.dump(response.json(), f)
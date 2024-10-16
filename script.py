import requests, time, hmac, hashlib, json

"""
BEFORE COMPILING THIS SCRIPT, YOU MUST FIRST COMPILE get_token.py TO GET A TOKEN FOR THE Tuya API.

After automation, file get_token.py will not be needed, because the token will be refreshed with refresh_token.py every 2 hours. 
So I didn't include code here to avoid doubling the number of requests each time. (Request to control device + unnecessary Request to get token)
If you forget to update the token within 2 hours, you need to get a new one using get_token.py.
"""

### Get data about solar panels via SolaxCloud API

"""
REPLACE THE DATA BELOW
"""

solax_tokenID = "token_ID"      ### Replace with your Token ID obtained in App or https://global.solaxcloud.com -> Service -> API 
sn = "sn"                       ### Replace with registration number of your inverter obtained in App or https://global.solaxcloud.com -> Device -> Inverter -> Registration No. column

### GET request to obtain information about Battery capacity (soc)
try: 
    response = requests.get(f"https://global.solaxcloud.com/proxyApp/proxy/api/getRealtimeInfo.do?tokenId={solax_tokenID}&sn={sn}")
except Exception as e:
    print(e)

soc = response.json()["result"]["soc"]

### If battery capacity lower than 15% ===> Turn on the smart socket (relay), which turns on the power supply from the electrical grid
### The socket is turned on using the Tuya API

if soc <= 15:
    print(f"Soc: {soc}%")

    ### Signature algorithm
    def generate_signature(client_id, client_secret, access_token, current_time, url, body):
        http_method = "POST"
        content_sha256 = hashlib.sha256(body.encode('utf-8')).hexdigest()
        string_to_sign = f"{client_id}{access_token}{current_time}{http_method}\n{content_sha256}\n\n{url}"
        signature = hmac.new(client_secret.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest().upper()    
        return signature

    ### Body for POST request to turn on the socket 
    body = '{"commands":[{"code":"switch_1","value":true}]}'

    ### Read token_file to get access token
    try:
        with open("token.json", "r") as file:
            token_file = json.load(file)
    except Exception as e:
        print(e)

    access_token = token_file["result"]["access_token"]     ### Read access token from imported json file 
    
    """
    REPLACE THE DATA BELOW
    """

    client_id = "client_id"                                 ### Replace with your Cliend ID obtained in the section Authorization in Smart Home cloud project
    client_secret = "client_secret"                         ### Replace with your Client Secret obtained in the section Authorization in Smart Home cloud project
    device_id = "device_id"                                 ### Replace with Device ID, you want to control, obtained in the section Devices 

    timestamp = str(int(time.time() * 1000))                ### UTC 13-digits timestamp used to generate signature
    url_path = f"/v1.0/devices/{device_id}/commands"        ### URL for POST request to Control Device
    signature = generate_signature(client_id, client_secret, access_token, timestamp, url_path, body)   ### Generate signature for the request


    ### Headers for the request
    headers = {
        "client_id": client_id,
        "sign": signature,
        "t": timestamp,
        "sign_method": "HMAC-SHA256",
        "access_token": access_token
    }

    ### POST request with initialized body and headers 
    try:
        response = requests.post(f"https://openapi.tuyaeu.com{url_path}", data=body, headers=headers)
    except Exception as e:
        print(e)

    ### For Debugging purposes
    print(f"Response: {response.json()}") ### Print the response from the API

else:
    print(f"Soc: {soc}%")
    print("Battery capacity greater than 15%")
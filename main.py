import hashlib
import requests
import json
import http.client
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.request import urlopen
import ssl
# print(urlopen('https://www.howsmyssl.com/a/check').read())

url = "https://192.168.100.190:8089/api"
user = "cdrapi"
conn = http.client.HTTPSConnection("192.168.100.190", 8089 , key_file=None, cert_file=None )
headers = {
    'Content-Type': 'application/json',


}


# payload = json.dumps({
#   "request": {
#     "action": "challenge",
#     "user": user,
#
#   }
# })

def get_token():
    payload = json.dumps({
        "request": {
            "action": "challenge",
            "user": user,
            "version": "1.2"

        }
    })
    conn.request("POST", "/api", payload, headers)
    res = conn.getresponse()
    res_in_by = res.read()
    res_in_json = res_in_by.decode('utf8').replace("'", '"')

    response = json.loads(res_in_json)
    cha = response['response']['challenge']
    # challenge = requests.request("POST", url, headers=headers, data=payload).json()
    # cha = challenge['response']['challenge']
    # # challenge = "0000001079540045"
    # # cha = "0000001376751561"
    salt = "cdrapi123"

    db_password = cha + salt

    token = hashlib.md5(db_password.encode())
    # print(token.hexdigest())
    return token.hexdigest()


def login():
    payload = json.dumps({
        "request": {
            "action": "login",
            "token": get_token(),
            "url": "http://192.168.100.190:8089",
            "user": "cdrapi"
        }
    })
    # response = requests.request("POST", url, headers=headers, data=payload).json()
    # return response['response']['cookie']
    conn.request("POST", "/api", payload, headers)
    res = conn.getresponse()

    res_in_by = res.read()
    res_in_json = res_in_by.decode('utf8').replace("'", '"')

    response = json.loads(res_in_json)
    return response['response']['cookie']



def cdr():
    payload = json.dumps(
        {"request": {

            "action": "cdrapi",

            "cookie": login(),

            "format": "json"

        }

        }
    )
    # response = requests.request("POST", url, headers=headers, data=payload)
    # print(response['response']['cookie'])
    conn.request("POST", "/api", payload, headers)
    res = conn.getresponse()
    res_in_by = res.read()
    res_in_json = res_in_by.decode('utf8').replace("'", '"')

    response = json.loads(res_in_json)
    cdr_report = (response['cdr_root'])
    print(cdr_report)
    for call in cdr_report:
        if 'main_cdr' in call:
         print(call)
cdr()



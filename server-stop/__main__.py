import os
import hashlib
import hmac
import base64
import requests
import time
import json
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

    ############# 참고 URL : https://api.ncloud-docs.com/docs/compute-vserver-server-startserverinstances
    ############# 요청 예시 ##############################################################################
    ############# GET {API_URL}/startServerInstances?regionCode=KR&serverInstanceNoList.1=***4299 #######
    ##################################################################################################### 
    ############# 한국, 국내용으로 regionCode KR로 고정

def stop_server(serverInstanceID, access_key, secret_key,api_url):
    
    method = "GET"
    
    uri = f"/vserver/v2/stopServerInstances?regionCode=KR&serverInstanceNoList.1={serverInstanceID}"
 
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    
    secret_key = bytes(secret_key, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    
    http_header = {
        'x-ncp-apigw-signature-v2': signingKey,
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
    }
    response = requests.get(api_url + uri, headers=http_header)
    
    if response.status_code == 200:
        try:
            return {"result": "success", "message": "Server stop request successful."}
        except json.JSONDecodeError:
            return {"result": "error", "message": "Invalid JSON format in the response."}
    else:
        return {"result": "error", "message": f"Failed to stop server Status code: {response.status_code}, Response: {response.text}"}


def main(args):
    access_key = args['NCLOUD_ACCESS_KEY']
    secret_key = args['NCLOUD_SECRET_KEY']
    server_instance_id = args['SERVER_INSTANCE_ID']
    api_url = "https://ncloud.apigw.ntruss.com"

    for i in server_instance_id:
        result = stop_server(i, access_key, secret_key,api_url)

    return result

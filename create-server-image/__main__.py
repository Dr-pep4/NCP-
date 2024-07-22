import os
import hashlib
import hmac
import base64
from urllib import response
import requests
import time
import json
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET



def create_server_image(instance_id, access_key, secret_key, server_name):


    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    


    secret_key = bytes(secret_key, 'UTF-8')
    method = "GET"
    api_server = "https://ncloud.apigw.ntruss.com"
    uri = f"/vserver/v2/getServerImageList?regionCode=KR&serverImageName={server_name}&responseFormatType=xml"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    http_header = {
        'x-ncp-apigw-signature-v2': signingKey,
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
    }
    response = requests.get(api_server + uri, headers=http_header)
    root = ET.fromstring(response.text)

# 필요한 정보 추출
    server_image_list = root.findall(".//serverImageList/serverImage")
    existed_images = root.find(".//totalRows")
    total_rows = int(existed_images.text)

    if server_image_list is not None:
        for server_image in server_image_list:
            server_image_no = server_image.find("serverImageNo").text
            server_image_name = server_image.find("serverImageName").text
            server_image_status_name = server_image.find("serverImageStatusName").text
            create_date = server_image.find("createDate").text

            print(f"Server Image No: {server_image_no}")
            print(f"Server Image Name: {server_image_name}")
            print(f"Server Image Status: {server_image_status_name}")
            print(f"Create Date: {create_date}")
            
    else:
        print("Server Image not found in the XML data.")

    total_rows_element = root.find(".//totalRows")
    total_rows = int(total_rows_element.text) if total_rows_element is not None else 0
    print(f"Total Rows: {total_rows}")







def main(args):
    access_key = args['NCLOUD_ACCESS_KEY']
    secret_key = args['NCLOUD_SECRET_KEY']
    server_name = args['SERVER_NAME']
    server_instance_id = args['SERVER_INSTANCE_ID']
   
    instance_id_to_create_image = server_instance_id
    result = create_server_image(instance_id_to_create_image, access_key, secret_key, server_name)
    
    print(result)
    return(result)

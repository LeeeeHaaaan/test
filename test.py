import requests
import os
import time
import json


def filescan(apikey, filepath):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': apikey}
    files = {'file': (filepath, open(filepath, 'rb'))}
    response = requests.post(url, files=files, params=params)

    return response.json()["resource"]


def file_report(API_key, file_resource):

    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': API_key, 'resource': file_resource}
    response = requests.get(url, params=params)


    return response.json()



API_key = "0979d6d9d1ee91ec24990660a906163aad5d6555f854a23363d5eb6c54d1461b"
filepath = "D:\\Data\\train\\dataset\\PE\\train_dataset_pe\\train_dataset_pe\\"


# file_resource = filescan(API_key, filepath)
# filedata = file_report(API_key, file_resource)

# for i, j in filedata["scans"].items():
#     result = filedata["scans"][i]["result"]
#     if result != None:
#         print(result)

files = os.listdir(filepath)

for filename in files:
    file = filepath + filename
    file_resource = filescan(API_key, file)


    filedata = file_report(API_key, file_resource)

    for i,j in filedata["scans"].items():
        result = filedata["scans"][i]["result"]
        if result != None:
            print(result)

    time.sleep(60)

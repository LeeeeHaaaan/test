import requests
import http.cookies


def create():
    REST_URL = "http://163.152.127.42:8001/tasks/create/file"
    SAMPLE_FILE = "D:/Data/train/dataset/00bc38c4f52c59864994581fb4c92006.vir"
    HEADERS = {"Authorization": "Bearer rzySNpEFSxRKZhHlY5q1Ew"}

    with open(SAMPLE_FILE, "rb") as sample:
        files = {"file": (SAMPLE_FILE.split("/")[-1], sample)}
        res = requests.post(REST_URL, headers=HEADERS, files=files)

    result = res.json()["task_id"]

    return result


def get_report():
    REST_URL = "http://163.152.127.42:8001/tasks/report/26"
    HEADERS = {"Authorization": "Bearer rzySNpEFSxRKZhHlY5q1Ew"}


    res = requests.get(REST_URL, headers=HEADERS)

    result = res.json()["behavior"]["processes"]

    return result

for i in get_report():
     for k in i["calls"]:
         print(k["api"])


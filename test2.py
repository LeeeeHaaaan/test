import requests

REST_URL = "http://163.152.127.42:8000/tasks/create/file"
SAMPLE_FILE = "D:/Data/train/dataset/00bc38c4f52c59864994581fb4c92006.vir"
HEADERS = {"Authorization": "Bearer S4MPL3"}
csrftoken = "oXToH5vwVu0U8KaHmWZiYR15CgI1Pxsu"

cookie = {
    "csrftoken" : csrftoken

}

with open(SAMPLE_FILE, "rb") as sample:
    files = {"file": ("sample", sample)}

    with requests.Session() as s:
        res = s.post(REST_URL, cookies=cookie, files=files)

result = res.json()["task_id"]
print(result)

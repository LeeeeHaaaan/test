import re

filepath = "C:\\Users\\dfrc\\Downloads\\저작권\\IP 정리.txt"

with open(filepath, "r", encoding="utf-8") as f:
    rr = re.findall("^([1-9]?\d|1\d{2}|2([0-4]\d)|25[0-5])\.){3}([1-9]?\d|1\d{2}|2([0-4]\d)|25[0-5])$", f.read())
    print(rr)

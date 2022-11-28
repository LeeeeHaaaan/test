from datetime import datetime

#35.50655
#129.43270

n = "35:31.703 N"
e = "129:33.540 E"

epoch_start = datetime.datetime(1601, 1, 1)
delta = datetime.timedelta(microseconds=int(webkit_timestamp))
return epoch_start + delta


if n.split(" ")[1] == "W" or "S"
angle = int(n.split(" ")[0].split(":")[0])


value = n.split(" ")[0].split(":")[1]
minute = int(value.split(".")[0])


value = float(value)
seconds = value - int(value)

seconds = round((round(seconds,3) * 60), 2)


result = angle + minute/60 + seconds/3600
print(round(result, 5))



angle = int(e.split(" ")[0].split(":")[0])


value = e.split(" ")[0].split(":")[1]
minute = int(value.split(".")[0])


value = float(value)
seconds = value - int(value)

seconds = round((round(seconds,3) * 60), 2)


result = angle + minute/60 + seconds/3600
print(round(result, 5))
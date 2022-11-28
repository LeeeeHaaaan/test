import SAMYOUNG_Navis3800_5100_track_parser as getTrack

filepath = "D:\\WaterPolice\\Navis3800\\tmp\\navis3800\\navis3800\\p1bfdd244c5b5a4ed6a6a010525f289db3\\T4000.dat"
trackData = getTrack.track(filepath)


getTrackData = []

filepath1 = "C:\\Temp\\test.txt"
with open(filepath1, "w") as f:
    for i in trackData:
        f.write(str(i[0]) + "," + str(i[1]) + "," + str(i[2]))
        f.write("\n")

print("12344")




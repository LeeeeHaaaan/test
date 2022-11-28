def trans_dms(value):
    # value /= 3600000
    #
    # degree = int(value)
    # arc_minute_sec = (value - degree) * 60
    # arc_min = int(arc_minute_sec)
    # arc_sec = round((arc_minute_sec - arc_min) * 60, 1)
    #
    # dms = str(degree) + "°" + str(arc_min) + "'" + str(arc_sec) + '"'
    dms = round(value / 3600000, 6)
    return dms

def navis3800_5100_track_extract(fname, path):
    with open(fname, 'rb') as fd:
        fd.seek(0x220000)
        data = fd.read()

    i = num = 0
    while data[i:i+8] != b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF':
        i += 8
        num += 1
    st = 22

    SIG = b'\xDC\xFE'

    with open(path, 'wb') as f:
        f.write(SIG)
        f.write(num.to_bytes(2, byteorder='little'))
        f.write(data[0:i+8])


def track(filename):
    with open(filename, 'rb') as fd:
        data = fd.read()

    ### PARSE ###
    header = data[:2]
    if header == b'\xdc\xfe':
        offset = 0
        num = int.from_bytes(data[0x2:0x4],'little')
        trackList = []

        for i in range(0, num):
            lat_raw = int.from_bytes(data[offset:offset+4], 'little')
            offset += 4
            lat = 8 * (lat_raw & 0x7ffffff) - 324000000
            lat = trans_dms(lat)
            connected = (lat_raw & 0xf8000000) >> 27
            lon_law = int.from_bytes(data[offset:offset+4], 'little')
            offset += 4
            lon = 8 * (lon_law & 0xfffffff)
            lon = trans_dms(lon)
            color = (lon_law & 0xf0000000) >> 28

            temp = [lat, lon, connected != 0, color]
            trackList.append(temp)

        return trackList


    else:
        return -1

# def sd_track(filename, fo="tmp"):
#     with open(filename, 'rb') as f:
#         data = f.read()
#
#     ### PARSE ###
#     header = data[:16]
#     size = data[16:16+20]
#     offset = 36
#     trackList = []
#
#     for i in range(1, 10):
#         s = int.from_bytes(size[i*2:i*2+1], 'little')
#         print("Page-%d Track-Size: %5d\n"%(i, s))
#         for j in range(1, s):
#             v11 = int.from_bytes(data[offset:offset+4], 'little')
#             offset += 4
#             v10 = 8 * (v11 & 0x7ffffff) - 324000000
#             v8 = (v11 & 0xf8000000) >> 27
#             v11 = int.from_bytes(data[offset:offset+4], 'little')
#             offset += 4
#             v9 = 8 * (v11 & 0xfffffff)
#             v7 = (v11 & 0xf0000000) >> 28
#
#             print("LAT: %15.10f, LON: %15.10f Connected: %d, COLOR: %2d"%(v10/3600000, v9/3600000, v8!=0, v7)) # latitude, longitude, v8!=0, v7
#             temp = [ round(v10/3600000, 6), round(v9/3600000, 6), v8!=0, v7 ]
#             trackList.append(temp)
#
#         print("\n\n")
#
#     return trackList
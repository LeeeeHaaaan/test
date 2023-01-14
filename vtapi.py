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


def n100A_track_parser(filename):

    with open(filename, "rb") as f:
        data = f.read()
        size = data[16:16+20]
        offset = 36
        convert_data = list()

        for i in range(10):

            s = int.from_bytes(size[2*i:2*i+2], 'little')

            for j in range(s):

                LAT_raw = int.from_bytes(data[offset:offset+4], 'little')
                offset += 4
                LAT = trans_dms((8 * (LAT_raw & 0x7ffffff) - 324000000))
                Connected = (LAT_raw & 0xf8000000) >> 27

                LON_raw = int.from_bytes(data[offset:offset+4], 'little')
                offset += 4
                LON = trans_dms((8 * (LON_raw & 0xfffffff)))
                Color = (LON_raw & 0xf0000000) >> 28
                convert_data.append((LAT, LON, Connected != 0, Color, LAT_raw, LON_raw))

        return convert_data

print(n100A_track_parser("D:\\WaterPolice\\spa-900 dataset\\FILE08\\test.DAT"))
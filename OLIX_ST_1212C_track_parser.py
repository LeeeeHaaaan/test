# Coding by YES, mingming
import tkinter

from pyproj import transform, Proj


#Path - /root/media/0/stella/Userdata/
#TrackParser
def trackparser(path):
    with open(path, 'rb') as tck:
        data = tck.read()

    degreelist = list()
    WGS84_LL = {'proj': 'latlong', 'ellps':'WGS84', 'datum':'WGS84'}
    TOKYO_LL = {'proj': 'latlong', 'ellps': 'bessel', 'towgs84': '-145.907,505.034,685.756'}
    header = data[0:2]
    coo_system = data[2:4]

    if header == b'\x81\x03':
        if coo_system == b'\x02\x00':
            coo_system = 'Tokyo'
        elif coo_system == b'\x00\x00':
            coo_system = 'WGS_84'

        start = 0x04
        for i in range((len(data)-4)//16):
            end = start + 0x10

            if data[start:start+4] == b'\xff\xff\xff\xff':
                break

            # lon_raw = int.from_bytes(data[start:start+4],'little') / 600000
            # lat_raw = int.from_bytes(data[start+4:start+8],'little') / 600000

            lon_raw = round(int.from_bytes(data[start:start+4],'little') /600000.0, 5)
            lat_raw = round(int.from_bytes(data[start+4:start+8],'little') / 600000.0, 5)

            if coo_system == 'Tokyo':
                lon_raw, lat_raw = transform(Proj (**TOKYO_LL), Proj (**WGS84_LL), lon_raw, lat_raw)

            connected = data[end-1]
            degreelist.append((coo_system, lat_raw, lon_raw, connected != 0))

            start = end

        return degreelist


#WPT parser
def wptparser(path):
    with open(path + 'wpt.dat', 'rb') as wpt:
        data = wpt.read()
        degreelist = list()

        if data[0:4] == b'\x20\x83\x31\x10':
            for i in range(int(len(data)/72)):
                t = i
                i = i * 72 + 8

                if data[4] == 1:
                    d = 'Tokyo'
                elif data[4] == 0:
                    d = 'wgs84'

                index = data[i]
                if t != 0 and index == 0:
                    break

                lat_raw = int.from_bytes(data[i+36:i+40], 'little')
                long_raw = int.from_bytes(data[i+40:i+44], 'little')
                lat = round(lat_raw / 3600000, 6)
                lon = round(long_raw / 3600000, 6)

                hour = str(int.from_bytes(data[i+56:i+58],'little'))
                mon = str(data[i + 58])
                day = str(data[i + 59])
                h = str(data[i + 60])
                min = str(data[i + 61])
                sec = str(data[i + 61])

                ptime = hour + '-' + mon + '-' + day + 'T' + h + ':' + min + ':' + sec + "Z"

                if index == 0 and ptime == 0:
                    break

                degreelist.append((index, d, lat, lon, ptime))
        else:
            return False

        return degreelist
from dfvfs.lib import definitions
from dfvfs.path import factory
from dfvfs.path.ntfs_path_spec import NTFSPathSpec
from dfvfs.resolver import resolver
from dfvfs.vfs.ntfs_data_stream import NTFSDataStream
import collections
import uuid
from urllib3.connectionpool import xrange
import struct
import sqlite3
from dfvfs.path.ewf_path_spec import EWFPathSpec

GPT_HEADER_FORMAT = """
8s signature
4s revision
L header_size
L crc32
4x _
Q current_lba
Q backup_lba
Q first_usable_lba
Q last_usable_lba
16s disk_guid
Q part_entry_start_lba
L num_part_entries
L part_entry_size
L crc32_part_array
"""

GPT_PARTITION_FORMAT = """
16s type
16s unique
Q first_lba
Q last_lba
Q flags
72s name
"""

file_path = 'D:\\test.E01'
save_path = 'D:\\testE01\\'

def _make_fmt(name, format, extras=[]):
    type_and_name = [l.split(None, 1) for l in format.strip().splitlines()]
    fmt = ''.join(t for (t,n) in type_and_name)
    fmt = '<'+fmt
    tupletype = collections.namedtuple(name, [n for (t,n) in type_and_name if n!='_']+extras)
    return (fmt, tupletype)

class GPTError(Exception):
    pass

def read_header(fp, lba_size=512):
    # skip MBR

    fp.seek(4096 + 1*lba_size)
    fmt, GPTHeader = _make_fmt('GPTHeader', GPT_HEADER_FORMAT)
    data = fp.read(struct.calcsize(fmt))
    header = GPTHeader._make(struct.unpack(fmt, data))
    if header.signature != b'EFI PART':
        raise GPTError('Bad signature: %r' % header.signature)
    if header.revision != b'\x00\x00\x01\x00':
        raise GPTError('Bad revision: %r' % header.revision)
    if header.header_size < 92:
        raise GPTError('Bad header size: %r' % header.header_size)
    # TODO check crc32
    header = header._replace(
        disk_guid=str(uuid.UUID(bytes_le=header.disk_guid)),
        )
    return header

def read_partitions(fp, header, lba_size=512):
    fp.seek(4096 + header.part_entry_start_lba * lba_size)
    fmt, GPTPartition = _make_fmt('GPTPartition', GPT_PARTITION_FORMAT, extras=['index'])
    for idx in xrange(1, 1+header.num_part_entries):
        data = fp.read(header.part_entry_size)
        if len(data) < struct.calcsize(fmt):
            raise GPTError('Short partition entry')
        part = GPTPartition._make(struct.unpack(fmt, data) + (idx,))
        if part.type == 16*'\x00':
            continue
        part = part._replace(
            type=str(uuid.UUID(bytes_le=part.type)),
            unique=str(uuid.UUID(bytes_le=part.unique)),
            # do C-style string termination; otherwise you'll see a
            # long row of NILs for most names
            name=part.name.decode('utf-16').split('\0', 1)[0],
            )
        yield part


def parser(file_path):
    with open(file_path, "rb") as f:
        header = read_header(f)
        for part in read_partitions(f, header):
            if part.name != '' and part.index == 4:     #파티션 index 강제 지정
                print(part.first_lba)
                return part.first_lba * 512

VBR_start_offset = parser(file_path)


def Find_FIle(file_path):
    FIle_Info = []
    os_path_spec = factory.Factory.NewPathSpec(definitions.TYPE_INDICATOR_OS, location=file_path)
    ewf_path_spec = factory.Factory.NewPathSpec(definitions.TYPE_INDICATOR_EWF, parent=os_path_spec)
    tsk_partition_path_spec = factory.Factory.NewPathSpec(definitions.TYPE_INDICATOR_TSK_PARTITION, location='/p4',parent=ewf_path_spec)
    ntfs_path_spec = NTFSPathSpec(definitions.TYPE_INDICATOR_NTFS, location='/', parent=tsk_partition_path_spec)
    file_entry = resolver.Resolver.OpenFileEntry(ntfs_path_spec)

    #디렉토리 검색 후 Log 파일 추출
    for sub_file_entry in file_entry.sub_file_entries:
        if sub_file_entry.name == "eNavigator2":
            for sub_file_entry1 in sub_file_entry.sub_file_entries:
                if sub_file_entry1.name == "VoyageLog":
                    for sub_file_entry2 in sub_file_entry1.sub_file_entries:
                        if sub_file_entry2.name == "log":
                            for sub_file_entry3 in sub_file_entry2.sub_file_entries:
                                print("파일명: " + sub_file_entry3.name + " 파일 사이즈: " + str(sub_file_entry3.size))

                                for i in sub_file_entry3.data_streams:
                                    for k in NTFSDataStream.GetExtents(i):
                                        print("NTFS VBR 시작으로부터 상대적 오프셋:",k.offset)
                                        FIle_Info.append([sub_file_entry3.name, sub_file_entry3.size , k.offset])


    return FIle_Info


def File_Carving(save_path, file_path, Logfile_info, VBR_start_offset):

    for file in Logfile_info:
        offset = file[2] + VBR_start_offset

        with open(file_path, "rb") as f:
            f.seek(offset)
            with open(save_path + file[0], "wb") as f_:  #파일 카빙
                f_.write(f.read(file[1]))


def save_sqlite(file_path, Logfile_info, VBR_start_offset):
    conn = sqlite3.connect("D:\\testE01\\test.db")


    for file in Logfile_info:
        st = str(file[0]).replace(".","")
        crsql = f"CREATE TABLE '{st}' (a text, b text, c text, d text, e text, f text, g text, h text, i text, j text, k text, l text, n text);"
        offset = file[2] + VBR_start_offset


        try:
            cur = conn.cursor()
            cur.execute(crsql)

        except sqlite3.Error as er:
            print(''.join(er.args))
            print(er.__class__)

        with open(file_path, "rb") as f:
            f.seek(offset)
            k = str(f.read(file[1])).split("\\r\\n")[:-1]

            for line in k:

                Info_list = line.split(",")
                insertsql = f"INSERT INTO '{st}' VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);"
                Info_list[0] = Info_list[0].replace("b'", " ").strip()

                #insertsql = f"INSERT INTO '{st}' Values('{Info_list[0]}','{Info_list[1]}','{Info_list[2]}','{Info_list[3]}','{Info_list[4]}','{Info_list[5]}', '{Info_list[6]}', '{Info_list[7]}', '{Info_list[8]}', '{Info_list[9]}', '{Info_list[10]}', '{Info_list[11]}', '{Info_list[12]}');"
                #print(insertsql)
                try:
                    cur = conn.cursor()
                    cur.execute(insertsql, (Info_list))


                except sqlite3.Error as er:
                    print(''.join(er.args))
                    print(er.__class__)

            conn.commit()

Logfile_info = list(Find_FIle(file_path))
#File_Carving(save_path, file_path, Logfile_info, VBR_start_offset)
#save_sqlite(file_path, Logfile_info, VBR_start_offset)
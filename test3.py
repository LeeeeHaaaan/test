from dfvfs.lib import definitions
from dfvfs.path import factory
from dfvfs.path.ntfs_path_spec import NTFSPathSpec
from dfvfs.path.gpt_path_spec import GPTPathSpec
from dfvfs.resolver import resolver
from dfvfs.lib.gpt_helper import GPTPathSpecGetEntryIndex
from dfvfs.lib import definitions
from dfvfs.path import factory
from dfvfs.resolver import resolver
from dfvfs.vfs.ntfs_data_stream import NTFSDataStream

location = 'D:\\test.E01'

os_path_spec = factory.Factory.NewPathSpec(definitions.TYPE_INDICATOR_OS, location=location)
ewf_path_spec = factory.Factory.NewPathSpec(definitions.TYPE_INDICATOR_EWF, parent=os_path_spec)
tsk_partition_path_spec = factory.Factory.NewPathSpec(definitions.TYPE_INDICATOR_TSK_PARTITION, location='/p4', parent=ewf_path_spec)
ntfs_path_spec = NTFSPathSpec(definitions.TYPE_INDICATOR_TSK, location='/',parent=tsk_partition_path_spec)

file_entry = resolver.Resolver.OpenFileEntry(ntfs_path_spec)

FIle_Info = []
for sub_file_entry in file_entry.sub_file_entries:
    if sub_file_entry.name == "eNavigator2":
        for sub_file_entry1 in sub_file_entry.sub_file_entries:
            if sub_file_entry1.name == "VoyageLog":
                for sub_file_entry2 in sub_file_entry1.sub_file_entries:
                    if sub_file_entry2.name == "log":
                        for sub_file_entry3 in sub_file_entry2.sub_file_entries:
                            # print("파일명: " + sub_file_entry3.name + " 파일 사이즈: " + str(sub_file_entry3.size))

                            for i in sub_file_entry3.data_streams:
                                for k in NTFSDataStream.GetExtents(i):
                                    print("NTFS VBR 시작으로부터 상대적 오프셋:",k.offset)
                                    FIle_Info.append([sub_file_entry3.name, sub_file_entry3.size, k.offset])






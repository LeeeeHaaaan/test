import os
import shutil

filepath = "D:\\Data\\train\\dataset\\PE\\train_dataset_pe\\train_dataset_pe"
allpath = "D:\\Data\\train\\dataset"

# pelist = os.listdir(filepath)
# alllist = os.listdir(allpath)

# a_sub_b = [x for x in alllist if x not in pelist and ".vir" in x]
#
# for i in a_sub_b:
#     shutil.move("D:\\Data\\train\\dataset\\" + i, "D:\\Data\\train\\ELF")


filepath1 = "D:\\Data\\Test\\test_dataset\\test_dataset\\"
filelist = os.listdir(filepath1)

elflist = 0

for i in filelist:
    with open(filepath1 + i, "rb") as f:
        if f.read(3) == b"\x7fEL":
            elflist += 1
            print(i, f.read(3))


#a_sub_b = [x for x in filelist if x not in elflist]

#for i in a_sub_b:
#    shutil.move("D:\\Data\\Test\\test_dataset\\test_dataset\\" + i, "D:\\Data\\Test\\test_dataset\\HTML_PE")
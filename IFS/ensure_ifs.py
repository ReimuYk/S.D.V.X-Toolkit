# python 3.5.3
# utf-8

# ensure guess correct for each .ifs file

import os

workpath = './result_chara/'
ifs_paths = []

def get_all_ifs_path():
    dir_list = os.listdir(workpath)
    ret = []
    for filename in dir_list:
        if os.path.isdir(workpath + filename):
            ret.append(workpath + filename + '/')
    return ret

def ensure_version_same():
    print("ensure_version_same: ", end = '\t')
    
    # read first file for baseline
    f = open(ifs_paths[0]+"version.xml", "rb")
    base = f.read()
    f.close()

    # compare others
    s_number = 0
    for fname in ifs_paths:
        f = open(fname+"version.xml", "rb")
        data = f.read()
        f.close()
        if data!=base:
            print("failed %s" % fname)
            return
        else:
            s_number += 1
    print("success! %d" % s_number)

def ensure_magic_same():
    print("ensure_magic_same: ", end = '\t')
    
    # read first file for baseline
    f = open(ifs_paths[0]+"magic", "rb")
    base = f.read()
    f.close()

    # compare others
    s_number = 0
    for fname in ifs_paths:
        f = open(fname+"magic", "rb")
        data = f.read()
        f.close()
        if data!=base:
            print("failed %s" % fname)
            return
        else:
            s_number += 1
    print("success! %d" % s_number)

def ensure_texturelist_same():
    print("ensure_texlist_same: ", end = '\t')
    
    # read first file for baseline
    f = open(ifs_paths[0]+"tex/texturelist.xml", "rb")
    base = f.read()
    f.close()

    # compare others
    s_number = 0
    for fname in ifs_paths:
        f = open(fname+"tex/texturelist.xml", "rb")
        data = f.read()
        f.close()
        if data!=base:
            print("failed %s" % fname)
            return
        else:
            s_number += 1
    print("success! %d" % s_number)

def ensure_raw_head_corr():
    print("ensure_raw_head: ", end = '\t')
    
    # 0x001FD110 & hex(filesize-8)
    s_number = 0
    for fname in ifs_paths:
        tex_dir = os.listdir(fname+"tex/")
        tex_dir.remove("texturelist.xml")
        rawname = tex_dir[0]
        f = open(fname+"tex/"+rawname, "rb")
        data = f.read()
        f.close()
        if data[0]!=0x00 or data[1]!=0x1f or data[2]!=0xd1 or data[3]!=0x10:
            print("failed front %s" % fname)
            return
        if ((data[4]<<24) | (data[5]<<16) | (data[6]<<8) | (data[7])) != len(data)-8:
            print("failed back %s" % fname)
            return
        s_number += 1
    print("success! %d" % s_number)

def ensure_raw_stru_corr():
    print("ensure_raw_stru: ", end = '\t')

    # raw: head(8bytes) | mask(1bytes) | payload(8+1 in mask bytes) | ... | end |
    # payload (1bytes): rel_data(1bytes)
    # payload (2bytes): repeat offset(12 bits) | repeat len - 3(4 bits)
    # end(as 2bytes payload): repeat offset == 0

    # total rel_data size: 2085136
    s_number = 0
    for fname in ifs_paths:
        # read a file
        tex_dir = os.listdir(fname+"tex/")
        tex_dir.remove("texturelist.xml")
        rawname = tex_dir[0]
        f = open(fname+"tex/"+rawname, "rb")
        data = f.read()
        f.close()

        # assert values
        rel_data_length = 2085136

        # jump head
        data = data[8:]

        # targets
        data_length = 0

        # walk through data
        cursor = 0

        raw_length = len(data)
        while cursor<raw_length:
            mask = data[cursor]
            cursor += 1
            for i in range(8):
                flag = mask & (1<<i) # flag=0 for 2bytes payload
                if flag:
                    data_length += 1
                    cursor += 1
                else:
                    if data[cursor]==0 and (data[cursor+1]&0xF0)==0:
                        cursor += 2
                        if cursor<raw_length:
                            print("failed raw_length %s %d" % (fname, cursor))
                            return
                        break
                    data_length += (data[cursor+1] & 0x0F) + 3
                    cursor += 2
        if cursor!=raw_length:
            print("failed raw_length2 %s" % fname)
            return
        if data_length!=rel_data_length:
            print("failed rel_data_length %s" % fname)
            return
        s_number += 1
    print("success! %d" % s_number)
    
    

ifs_paths = get_all_ifs_path()
if ifs_paths==[]:
    print("Warning: IFS list empty")
else:
    ensure_version_same()
    ensure_magic_same()
    ensure_texturelist_same()
    ensure_raw_head_corr()
    ensure_raw_stru_corr()

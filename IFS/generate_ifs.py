from PIL import Image
import numpy as np
import time
import sys

def simple_Image2Raw(image):
    # warning: this function has no compress
    img_arr = np.array(image)

    w = len(img_arr)
    h = len(img_arr[0])

    ret = []
    flag = True
    for x in range(w):
        for y in range(h):
            if flag:
                ret.append(255)
            px = img_arr[x][y]
            ret.append(px[2])
            ret.append(px[1])
            ret.append(px[0])
            ret.append(px[3])
            flag = not flag
    ret.append(0)
    ret.append(0)
    ret.append(0)

    l = len(ret)
    ret = [0x00, 0x1f, 0xd1, 0x10, l>>24 & 0xff, l>>16 & 0xff, l>>8 & 0xff, l & 0xff] + ret
    return bytes(ret)

def pack_ifs(image):
    # header
    f = open("./assets/header", "rb")
    header = f.read()
    f.close()

    # raw
    rawdata = simple_Image2Raw(image)

    # texturelist.xml
    f = open("./assets/texturelist.xml", "rb")
    texture = f.read()
    f.close()

    # version.xml
    f = open("./assets/version.xml", "rb")
    version = f.read()
    f.close()

    return header + rawdata + texture + version

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: No input image file.")
        exit()
    in_name = sys.argv[1]
    if in_name[-4:]!='.png':
        print("Error: Only PNG file can be input")
        exit()
    out_name = "output.ifs"
    img = Image.open(in_name)
    data = pack_ifs(img)
    f = open(out_name, "wb")
    f.write(data)
    f.close()
    print("Success!")
    
    

    

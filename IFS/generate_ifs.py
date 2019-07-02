from PIL import Image
import numpy as np
import time

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

img = Image.open("hyq-end.png")
raw = simple_Image2Raw(img)
f = open("raw","wb")
f.write(raw)
f.close()
    

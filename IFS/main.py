from PIL import Image
import numpy as np
import time

def DecompressLSZZ(content):
    print(len(content))
    ret = []

    print(content[:8])
    content = content[8:]

    ctrlLen = 0
    ctrl = 0
    dect = []

    while (content):
        data = content[0]
        content = content[1:]

        if (ctrlLen == 0):
            ctrl = data
            ctrlLen = 8
            continue

        if ((ctrl & 0x01) == 0x01):
            ret.append(data)
            dect.append(data)
            ctrl = ctrl >> 1
            ctrlLen -= 1
            continue

        cmd0 = data
        cmd1 = 0

        if not content:
            break
        else:
            cmd1 = content[0]
            content = content[1:]

        chLen = (cmd1 & 0x0f) + 3
        chOff = ((cmd0 & 0xff) << 4) | ((cmd1 & 0xf0) >> 4)
        index = len(dect) - chOff


        dest = []
        i = 0
        while (i < chLen):
            if (index >= len(dect)):
                if (chOff == 0):
                    break
                index = len(dect) - chOff
            if (index < 0):
                ret.append(0)
                dest.append(0)
            else:
                decVal = dect[index]
                ret.append(decVal)
                dest.append(decVal)
            i += 1
            index += 1

        dect = dect + dest

        decSize = 0x1000
        if (len(dect) > decSize):
            dect = dect[len(dect) - decSize + 1 :]
        
        ctrl = ctrl >> 1
        ctrlLen -= 1

    return bytes(ret)

def Raw2Image(raw, h, w):
    # assert size correct
    if h*w*4 != len(raw):
        print("Raw2Image: incorrect size (%d, %d, %d)" % (len(raw), h, w))
        return

    image = Image.fromarray(np.array([[0]*h]*w)).convert('RGBA')
    img_arr = np.array(image)
    for x in range(w):
        for y in range(h):
            off = (x * w + y) * 4
            img_arr[x][y] = [raw[off+2], raw[off+1], raw[off], raw[off+3]]

    return Image.fromarray(img_arr)

def DecodeRaw(raw):
    filesize = len(raw)

    if (filesize==0 or filesize%4!=0):
        print("filesize error %d" % filesize)

    argbsize = filesize / 4
    argbarr = []

    for i in range(0, filesize, 4):
        argb_pixel = [raw[i+2], raw[i+1], raw[i], raw[i+3]]
        argbarr.append(argb_pixel)

    offset = 0
    if (argbarr[0] == 0x54584454):
        print("offset 16")
        offset = 16

    i2bset = {}
    for i in range(1, int(argbsize**0.5)):
        if (argbsize%i != 0):
            continue
        i2bset[i] = 0;
        i2bset[int(argbsize/i)] = 0

    indexsize = len(i2bset)
    widths = [0] * indexsize
    heights = [0] * indexsize
    k = 0

    keys = list(i2bset)
    keys = sorted(keys)

    for item in keys:
        widths[k] = item
        heights[indexsize - k - 1] = item
        k += 1

    return argbarr, widths, heights, offset

def CreateImg(argbarr, widths, heights, offset, index):
    img_w = 722
    img_h = 722
    image = Image.fromarray(np.array([[0]*img_h]*img_w)).convert('RGBA')
    img_arr = np.array(image)

    for y in range(img_h):
        for x in range(img_w):
            argb = argbarr[x*widths[index]//2 + y + off]
            img_arr[x][y] = argb

    image = Image.fromarray(img_arr)
    
    return image

begin_time = time.time()
f = open('./assets/raw','rb')
raw = DecompressLSZZ(f.read())
##argbarr, w, h, off = DecodeRaw(raw)
f.close()

##img = CreateImg(argbarr, w, h, off, 7)
img = Raw2Image(raw, 722, 722)
end_time = time.time()
print("cost: %d"%(end_time-begin_time))
##img.show()    

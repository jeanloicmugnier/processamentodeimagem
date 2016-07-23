from PIL import Image
import numpy as np
from PIL import ImageFilter
from  PIL.ImageFilter import Kernel

filter_suav = [1, 4, 6, 4, 1]
kernel_suav = 1. / 16* np.array([1, 4, 6, 4, 1,4,16,24,16,4,6,24,36,24,6,4,16,24,16,4,1,4, 6, 4, 1])
kernel_suav_exp = 4* kernel_suav

def remove_horizontal(img):
    x, y = img.size
    new2 = Image.new("RGBA", (x, y / 2))
    uc = 0
    dc = 0
    nc = 0
    while (dc < x):
        new = img.crop((0, uc, x, dc + 1))
        new2.paste(new, (0, nc))
        uc += 2
        dc += 2
        nc += 1
    return new2


# comeco da esquerda, x, fim pra direita, y
def remove_vertical(img):
    x, y = img.size
    new2 = Image.new("RGBA", (x / 2, y))
    lc = 0
    rc = 0
    nc = 0
    while (rc < x):
        new = img.crop((lc, 0, rc + 1, y))
        new2.paste(new, (nc, 0))
        lc += 2
        rc += 2
        nc += 1
    return new2

def blur2(img,kernel):
    # print(kernel)
    # print(len(kernel))
    # print(kernel[0].size)
    # print(kernel[1].size)
    return img.filter(Kernel((5,5),kernel))


def add_horizontal(img):
    x, y = img.size
    new2 = Image.new("RGBA", (x, y * 2))
    uc = 0
    dc = 0
    nc = 0
    while (dc < x):
        new = img.crop((0, uc, x, dc + 1))
        new2.paste(new, (0, nc))
        uc += 1
        dc += 1
        nc += 2
    return new2


def add_vertical(img):
    print(img)
    x, y = img.size
    new2 = Image.new("RGBA", (x * 2, y))
    lc = 0
    rc = 0
    nc = 0
    while (rc < x):
        new = img.crop((lc, 0, rc + 1, y))
        new2.paste(new, (nc, 0))
        lc += 1
        rc += 1
        nc += 2
    return new2


def sum(img1, img2):
    x_max, y_max = img1.size
    new = Image.new(img1.mode, img1.size)
    for x in range(x_max):
        for y in range(y_max):
            pix1 = img1.getpixel((x, y))
            pix2 = img2.getpixel((x, y))
            l = []
            for i in range(3):
                val = pix1[i] + 4* pix2[i]
                val = val if (val <= 255) else 255
                l.append(val)

            new.putpixel((x, y), (l[0], l[1], l[2]))
    return new


# '''
# img1 and img2 must be the same size
# return img(img1 - img2)
# '''


# def diff(img1, img2):
#     x1, y1 = img1.size
#     x2, y2 = img1.size
#     # print("img1", img1.split()[0].size)
#     # print("img2", img2.split()[0].size)
#     # print("x1", x1,y1)
#     # print("x2", x2,y2)
#     if (x1 != x2 or y1 != y2):
#         print("IMAGES OF DIFERENT SIZE!!!")
#         exit(1)
#     a_len = x1 * y1
#     t_img1 = img1.split()
#     t_img2 = img2.split()
#     l_color = []

#     for i in range(3):
#         np_array = np.zeros(a_len)
#         c_img1 = np.array(t_img1[i].getdata())
#         c_img2 = np.array(t_img2[i].getdata())
#         # while(c_img1.size[0]<c_img2.size[0]):
#         #     c_img1.append(0,0,0)
#         # while(c_img1.size[0]<c_img2.size[0]):
#         #     c_img2.append(0,0,0)
#         for x in range(a_len):
#             if ((img2.size[0] < img1.size[0]) and x % (x2) == 0):
#                 c_img2 = np.insert(c_img2, x, 0)
#             if ((img2.size[1] < img1.size[1]) and x % (y2) == 0):
#                 c_img2 = np.insert(c_img2, x, 0)
#             # print("x",x)
#             # print(c_img2.size)
#             # print(c_img1.size)
#             di = c_img1[x] - c_img2[x]
#             np_array[x] = di if (di > 0) else 0
#         l_color.append(np_array)
#     res = Image.new("RGB", img1.size)
#     data = listb_to_img(l_color, x1 * y1, "RGB")
#     data = tuple(map(tuple, data))
#     res.putdata(data)

#     return res


def listb_to_img(lis, size, mode):
    at = np.zeros(size, dtype='int,int,int')

    for k in range(size):
        at[k] = (lis[0][k], lis[1][k], lis[2][k])
    return at

def diff_pixel(x_pixel, y_pixel):
    '''

    Makes the subtraction between two pixels in RGB mode.
    If a value of a band is lower than 0, then it is set to 0

    :param x_pixel: minuend pixel
    :param y_pixel: subtrahend pixel
    :return: the subtraction of x_pixel and y_pixel
    '''
    nb_pixel = 5
    new = np.zeros(nb_pixel)
    for ind in range(nb_pixel):
        diff = x_pixel[ind] - y_pixel[ind]
        new[ind] = 0 if (diff < 0 and ind > 1) else diff
    return new

def diff_img(img1,img2):
    # np_img1 = np.array(img1)
    # print(np_img1)
    x_max,y_max = img1.size
    # np_img1 = np_img1.reshape(1,np_img1.size/3,3)[0]
    # np_img2 = np.array(img2)
    # np_img2 = np_img2.reshape(1,np_img2.size/3,3)[0]
    # new=np.zeros(np_img1.size/3,tuple)
    new_img = Image.new(img1.mode, img1.size)
    # # print(new)
    for x in range(x_max):
        for y in range(y_max):
            l=[]
            pixel1 = img1.getpixel((x,y))
            pixel2 = img2.getpixel((x,y))
            # print("pixel1",pixel1)
            # print("pixel2",pixel2)
            for i in range(3):
                val = pixel1[i] - 4 * pixel2[i]
                val = 0 if(val<0) else val
                l.append(val)
            new_img.putpixel((x,y),tuple(l))
    # for i in range(np_img1.size/3):
    #     # print(np_img1[i])
    #     # print(np_img2)
    #     # print(np_img1[i])
    #     new[i] = np_img1[i]-np_img2[i]
    #     # print((i//x,i%y))
    #     # new_img.putpixel((i%x,i%y),tuple(new[i]))

    # # print(tuple(new))
    # # new_img = new_img.putdata(tuple(new))
    # new_img = Image.fromarray(new,"RGB")    
    # new_img.show()
    return new_img

def convolution(img, coef):
    global filter_suav
    x_max, y_max = img.size
    fsize = len(filter_suav)
    lt = []
    bands = img.split()
    # print(img.split())
    # print("3", bands[2])
    # print("2", bands[1])
    # print("1", bands[0])
    for y in range(y_max):
        for x in range(fsize):
            # print("y ",y," x ", x)
            lt.append(img.getpixel((x, y)))
        for x in range(fsize, x_max):
            l = []
            for color in range(3):
                acc = 0
                for fi in range(fsize):
                    global coeff
                    # print(x-fi,y)
                    # print(bands[color].getpixel((x - fi, y)))
                    acc = acc + (coeff * coef * bands[color].getpixel((x - fi, y)) * filter_suav[-1 - fi])
                    acc = int(acc) if (acc < 256) else 255
                l.append(acc)
            lt.append(tuple(l))
    imf = Image.new(img.mode, img.size)
    imf.putdata(lt)
    return imf


def convolution_vertical(img, coef):
    print("SIIIIIZEEE  ", img.size)
    global filter_suav
    x_max, y_max = img.size
    fsize = len(filter_suav)
    new = Image.new(img.mode, img.size)
    bands = img.split()
    #
    for x in range(x_max):

        for y in range(fsize):
            new.putpixel((x, y), img.getpixel((x, y)))
        for y in range(fsize, y_max):
            l = []
            # print("x",x,"\ny",y)
            for color in range(3):
                acc = 0
                for fi in range(fsize):
                    global coeff
                    # print('x ', x, " y ", y, " fi ", fi)
                    acc = acc + (coeff * coef * bands[color].getpixel((x, y - fi)) * filter_suav[-1 - fi])
                    acc = int(acc) if (acc < 256) else 255
                l.append(acc)
            new.putpixel((x, y), (l[0], l[1], l[2]))
    return new

def save_pics(name,list_img):
    for i in range(len(list_img)):
        list_img[i].save(name+str(i)+".jpeg", "JPEG")

def expand(img,coef):
    img = dobrar(img)
    img = blur2(img,kernel_suav_exp)
    # img.show()
    return img

def blur(img, coef):
    new = convolution(img, coef)
    new = convolution_vertical(new, coef)
    return new


def reduce(img):
    img = blur2(img, kernel_suav)
    img = remove_vertical(remove_horizontal(img))
    return img


def dobrar(img):
    img = add_horizontal(add_vertical(img))
    return img


def correlation(img, coef):
    global filter_suav
    x_max, y_max = img.size
    fsize = len(filter_suav)
    lt = []
    bands = img.split()
    leftend = x_max - fsize
    #
    for y in range(y_max):
        line = []
        for x in range(leftend):
            l = []
            for color in range(3):
                acc = 0
                for fi in range(fsize):
                    global coeff
                    acc = acc + (coef * coeff * bands[color].getpixel((x_max - x - fsize + fi, y)) * filter_suav[fi])
                    acc = int(acc) if (acc < 256) else 255
                l.append(acc)
            line.append(tuple(l))
        for x in range(fsize):
            line.insert(0, img.getpixel((fsize - x, y)))
        line.reverse()
        lt.append(line)
    lt = [val for sublist in lt for val in sublist]
    imf = Image.new(img.mode, img.size)
    imf.putdata(lt)
    return imf

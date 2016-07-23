import PIL.Image as IMG
import numpy as np
import  Image
from pixel import Pixel as pix
import PiramideLaplaciana


# maca = IMG.open("images/maca.jpg")
# lar = IMG.open("images/laranja.jpg")
# masc = IMG.open("images/mask_1_2.jpg")
# filter_suav = [1, 4, 6, 4, 1]
# coeff = 1. / 16
# # print(img.format,img.size,img.mode)
# x_maca, y_maca = maca.size
# x_lar, y_lar = lar.size
# i = 0
# box = (0, 0, 200, y_lar)
# t = maca.load()
# r, g, b = maca.split()
# pixel_size = 3

# new_masc = masc.convert("RGB")
# print(new_masc.mode)
# print(new_masc.split())
# # print(maca.getdata())
# # print(arr[200][200])
# # arr[arr < 10] = 0
# # print(arr[200])
# img = IMG.new("RGB", (x_maca, y_maca))


def piramide_gaussiana(img, levels):
    l_gau = []
    l_gau.append(img)
    for i in range(levels):
        l_gau.append(Image.reduce(l_gau[i]))
    return l_gau


def show_list_img(lis):
    for i in range(len(lis)):
        # print(lis[i].size)
        lis[i].show()



def merge_w_mask(img1, img2, mask):
    '''
    merge img1 and img2 according to mask
    '''
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    marr = np.array(mask)
    lt = np.zeros(arr1.size/pixel_size, tuple)
    i=0
    for line in range(arr1.size/arr1[0].size):
        for col in range(arr1[0].size/pixel_size):
            msc_d = marr[line][col]
            la_data = arr1[line][col]
            lb_data = arr2[line][col]
            l = np.zeros(3,int)
            for k in range(3):
                msc = msc_d[k]/255
                val1 = msc * la_data[k] 
                val2 = ((1 - msc) * lb_data[k])
                val_res = val1+val2
                val_res = val_res if (val_res > 0) else 0
                val_res = val_res if (val_res < 256) else 255
                val_res= int(val_res)
                l[k]= val_res
            lt[i] = tuple(l)
            i+=1
    new = IMG.new("RGB", img1.size)
    new.putdata(lt)
    return new

def mask_to_bin(mask):
    new = np.array(mask,tuple)
    print(new)
    for i in range(len(new)/pixel_size):
        new[i] = pix.mult_by_const(new[i],1./255) 

# def merge_with_mask(img1,img2,mask):
#     l=[] 
#     new = sum(limg1[i],limg2[i])
#     for i in range(limg1):
#         l.append(new)
#     return l

def bands_to_image(bands, size):
    l = []
    img1 = IMG.new("RGB", size)
    x = len(list(bands[0]))
    for k in range(x):
        l.append((bands[0][k], bands[1][k], bands[2][k]))
    # print(l)
    img1.putdata(l)
    return img1



# pixel_size = 3
# l = piramide_gaussiana(maca,2)
# lap = PiramideLaplaciana.piramide_laplaciana(l,2)
# # Image.save_pics("lap_",lap)
# c = PiramideLaplaciana.colapsar(lap, l[0])
# # merge_w_mask(maca, lar, new_masc).show()
# # l = merge_photos(maca, lar, new_masc)
# # l= colapsar([maca,lar])
# # show_list_img(l)

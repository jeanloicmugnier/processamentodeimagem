import PiramideGaussiana 
import PiramideLaplaciana 
from PIL import Image
import Image as img 
import numpy as np

kernel_suav = 1. / 16* np.array([1, 4, 6, 4, 1,4,16,24,16,4,6,24,36,24,6,4,16,24,16,4,1,4, 6, 4, 1])

def blend(img1,img2,masc,g_level):
    lg1 = PiramideGaussiana.piramide_gaussiana(img1,g_level)
    lg2 = PiramideGaussiana.piramide_gaussiana(img2,g_level)
    lg_masc = PiramideGaussiana.piramide_gaussiana(masc,g_level)    
    blur_masc = img.blur2(lg_masc[-1],kernel_suav)
    blur_masc = img.blur2(blur_masc,kernel_suav)
    blur_masc = img.blur2(blur_masc,kernel_suav)
    blur_masc = img.blur2(blur_masc,kernel_suav)

    pg_merged =merge_img_masc(lg1[-1],lg2[-1], blur_masc )
    lp1 = PiramideLaplaciana.piramide_laplaciana(lg1,g_level)
    lp2 = PiramideLaplaciana.piramide_laplaciana(lg2,g_level)
    ls = create_ls(lp1,lp2,lg_masc)
    return PiramideLaplaciana.colapsar(ls,pg_merged)

def merge_img_masc(img_a,img_b,img_masc):
    x_max,y_max = img_a.size
    new = Image.new(img_a.mode,img_a.size)
    # print("a ",img_a.size)
    # print("b ",img_b.size)
    # print("masc ",img_masc.size)
    # print("masc next ",msc[i+1].size)

    for x in range(x_max):
        for y in range(y_max):
            msc_d = img_masc.getpixel((x,y)) 
            pix_a = img_a.getpixel((x,y))
            pix_b = img_b.getpixel((x,y))
            pixel=[]

            for i in range(3):
                # print("size", pic1.size, "", msc_d)
                val = (msc_d[i]/255 * pix_a[i]) + ((1 - msc_d[i]/255) * pix_b[i])
                val = val if (val > 0) else 0
                val = val if (val < 256) else 255
                pixel.append(val)
            new.putpixel((x,y),tuple(pixel))
    # new.show()
    return new
def create_ls(la, lb, msc):
    

    lls = []
    msc.reverse()
    for i in range(len(la)):
        img_a = la[i]
        img_b = lb[i]
        img_masc = msc[i+1]
        # ls.append()

        new =merge_img_masc(img_a,img_b,img_masc)
        lls.append(new)
    # show_list_img(lls)
    # lls = piramide_laplaciana(lls, len(la))
    # show_list_img(lls)
    return lls

maca = Image.open("images/maca.jpg")
lar = Image.open("images/laranja.jpg")
masc = Image.open("images/mask_1_2.jpg")
new_masc = masc.convert("RGB")

l = blend(maca,lar,new_masc,2)
print(len(l))
img.save_pics("lol_",l)
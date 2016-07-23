import PIL.Image as IMG
import Image as mine_img
import numpy as np



def colapsar(pir_lap, last_gauss):
    c=[last_gauss]
    # pega os dois primeiros fora do loop
    # l.append(mine_img.sum(limg1[0], mine_img.expand(limg1[i])))
    # exp =mine_img.expand(last_gauss)
    for i in range(len(pir_lap)):
        print(i)
        # pir_lap[i].show()
        # mine_img.expand(c[i],4).show()
        new = mine_img.sum(pir_lap[i],mine_img.expand(c[i],1))
        new.show()
        c.append(new)
    return c



def piramide_laplaciana(l_gau, level):
    l_lap = []
    size = len(l_gau)
    l_gau.reverse()
    # l_gau[1].show()
    # mine_img.expand(l_gau[0],4).show()
    # mine_img.expand(l_gau[1],4).show()
    # l_lap.append(mine_img.diff_img(l_gau[1], mine_img.expand(l_gau[0],4)))
    for i in range(2, size+1):
        l_lap.append(mine_img.diff_img(l_gau[i-1], mine_img.expand(l_gau[i - 2],4)))
    return l_lap




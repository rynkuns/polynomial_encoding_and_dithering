# Szymon Rynkun

#%matplotlib inline
import numpy as np
from scipy import polyfit, polyval
from matplotlib.pyplot import *
from PIL import Image
from copy import deepcopy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-w","--wczyt", help="nazwa wczytywanego pliku pliku", default='skompresowany_SR.npy')
parser.add_argument("lgener", help="liczba klatek do wygenerowania", type=int)
parser.add_argument("-z","--zapis", help="nazwa zapisywanego pliku/plików", default='wygenerowane_SR')
parser.add_argument("-g","--gif", help="zapisuje GIFa zamiast plików PNG", action="store_true")
args = parser.parse_args()

wielomiany = np.load(args.wczyt)

wys, szer, _, _ = wielomiany.shape

remake = np.zeros((args.lgener, wys, szer, 3), dtype='u1')
ile = np.linspace(0,10,args.lgener)
for y in range(wys):
    for x in range(szer):
        for kolor in range(3):
            pixele =  polyval(wielomiany[y,x,kolor,],ile)
            for i in range(len(pixele)):
                remake[i, y, x, kolor] = pixele[i]
        

remake = np.clip(remake, 0, 255)
klatki = []
for n in range(args.lgener):
    obraz = Image.fromarray(remake[n], 'RGB')
    klatki.append(obraz)
    
if args.gif: #podobnie jak z encode - program pierwotnie generował tylko gify
    klatki[0].save(args.zapis+'.gif', format='GIF', append_images=klatki[1:], save_all=True, duration=100, loop=0)
else:
    for n in range(len(klatki)):
        klatki[n].save(args.zapis+str(n)+'.png', format='PNG')
        
    





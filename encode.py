# Szymon Rynkun

#%matplotlib inline
import numpy as np
from scipy import polyfit, polyval
from PIL import Image
from copy import deepcopy
from warnings import catch_warnings, simplefilter
from matplotlib.pyplot import *
import argparse
import fnmatch
import os


parser = argparse.ArgumentParser()
parser.add_argument("plik", help="ścieżka do / nazwa pliku GIF, lub folderu z plikami PNG")
parser.add_argument("kompresja", help="rząd wielomianu, służącego do aproksymacji pixeli (im mniejsza wartość tym większa kompresja, ale gorsza jakość odtworzonego obrazu)", type=int)
parser.add_argument("-z","--zapis", help="nazwa zapisywanego pliku", default='skompresowany_SR')
parser.add_argument("-g","--gif", help="wczytuje GIFa zamiast plików PNG", action="store_true")
parser.add_argument("-p","--pokaz", help="pokazuje na koniec kontrolną klatkę", action="store_true")
parser.add_argument("-f","--accu", help="precyzja zapisywanych wartości współczynników wielomianów aproksymujących (im większa liczba, tym bardziej precyzyjny wielomian kosztem większego zużycia pamięci",
                    default='f4', choices=['f2', 'f4', 'f8'])
args = parser.parse_args()

plik = args.plik
kompresja = args.kompresja

dane = []  #zmienna przechowująca informacje o obrazie w postaci [klatka][wiersz][kolumna][rgb]


if args.gif:
    surowe = Image.open(plik)
    szer, wys = surowe.size
    try:
        while True:
            obraz = deepcopy(surowe).convert('RGB')
            dane.append(np.array(obraz))
            surowe.seek(surowe.tell()+1)  #przejście do nast. klatki
    except EOFError: #przy braku kolejnej klatki
        lklat = surowe.tell()+1 #suma klatek
        print('wczytano',lklat, 'klatek') 
    del obraz#, klatka  #dla oszczędzenia pamięci z ostatniej klatki

else:  #program początkowo pisałem pod wczytywanie gifów i tak pierwotnie działał
    pngi = []
    for file in os.listdir(plik):
        if fnmatch.fnmatch(file, '*.png'):
            pngi.append(file)
    pngi = sorted(pngi)
    for nazwa in pngi:
        obraz = Image.open(nazwa)
        dane.append(np.array(obraz))
    szer, wys = obraz.size
        

ile = np.linspace(0,10,lklat)

with catch_warnings():
    simplefilter('default')
    try:
        wielomiany = np.zeros((wys, szer, 3, kompresja+1), dtype=args.accu) #pusta macierz, na przyszłe wielomiany
        for y in range(wys):
            for x in range(szer):
                for kolor in range(3):
                    seria=[]
                    for klatka in dane:
                        seria.append(klatka[y][x][kolor])
                    aprox = polyfit(ile,seria,kompresja)du
            
                    for i in range(kompresja+1):
                        wielomiany[y,x,kolor,i] = aprox[i]
                  
        if args.pokaz:      
            testowe = np.zeros((wys, szer, 3), dtype='u1')
            for yy in range(wys):
                for xx in range(szer):
                    for k in range(3):
                        testowe[yy,xx,k]=polyval(wielomiany[yy,xx,k,:], 5) #generuje jedną klatkę ze środka, w celach kontrolnych
        
            Image.fromarray(testowe).show()

                        
    except np.RankWarning:
            pass             



np.save(args.zapis, wielomiany)




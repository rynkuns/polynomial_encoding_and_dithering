# Szymon Rynkun
# 2019

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

print('\n Szymon Rynkun | 2019\n Program do redukcji liczby kolorów\n\n')

plik = input('Podaj ścieżkę pliku (w foracie PNG) >>')
l_klast = int(input('Do ilu zredukować liczbę kolorów? >>'))
czy_FSteinberg = 'xd'
while czy_FSteinberg not in ['T', 'N', 'Y']:
    czy_FSteinberg = input('Czy cieniować metodą Floyda-Steiberga? (T|N)>>').upper()
if czy_FSteinberg in ['T', 'Y']: czy_FSteinberg = True
else: czy_FSteinberg = False


obraz = Image.open(plik).convert("RGB") #konwersja do RGB
pixele = [] #lista pierwotnych wartości pixeli z danego obrazu

for y in range(obraz.size[1]):
    for x in range(obraz.size[0]):
        pixele.append(obraz.getpixel((x,y)))
        
klastry = KMeans(n_clusters=l_klast, random_state=0).fit(pixele) #klastrowanie

indeks = klastry.labels_ #lista, do któego klastra należy dany pixel
kolor = klastry.cluster_centers_.astype(int) #wybrane przezalgorytm kolory
mapa = obraz.load() 
        
        
if czy_FSteinberg:
    def korektor(pierwotny, korekta, waga):
        """Funkcja przyjmuje wartość pierwotną pixela, oraz wyliczoną wartość błędu z poprzedniego pixela,
           a następnie aplikuje ją z odpowiednią wagą i zwraca."""
        nowy = []
        for i in range(3):
            nowy.append(int(pierwotny[i] + korekta[i]*waga))
        return tuple(nowy)
        

    for y in range(obraz.size[1]-1):       #faktyczny proces cieniowa algorytmem
        for x in range(1,obraz.size[0]-2):
            oryginalny = obraz.getpixel((x,y))
            nowy = kolor[klastry.predict(np.array(oryginalny).reshape(1, -1))][0]
            mapa[x,y] = tuple(nowy)
            buond = np.array([oryginalny[0] - nowy[0], oryginalny[1] - nowy[1], oryginalny[2] - nowy[2]]) #błąd przybliżenia (w skali RGB)
            mapa[x+1,y] = korektor(obraz.getpixel((x+1,y)), buond, 7/16)
            mapa[x-1,y+1] = korektor(obraz.getpixel((x-1,y+1)), buond, 3/16)
            mapa[x,y+1] = korektor(obraz.getpixel((x,y+1)), buond, 5/16)
            mapa[x+1,y+1] = korektor(obraz.getpixel((x+1,y+1)), buond, 1/16)
            #powyżej dodawanie wartości błędu do sąsiadujących pixeli (zgodnie z algorytmem)
            
else: #redukcja l. kolorów bez cieniowania
    n = 0
    for y in range(obraz.size[1]):
        for x in range(obraz.size[0]):
            mapa[x,y] = tuple(kolor[indeks[n]])
            n+=1

obraz.show()
print('\n Czy chcesz zapisać obraz?')
czy_zapis = 'xd'
while czy_zapis not in ['T', 'N', 'Y']:
    czy_zapis = input('(T|N)>>').upper()
if czy_zapis in ['T', 'Y']:
    lokalizacja = input('Lokalizacja (w tym nazwa wraz z rozszerzeniem) nowego pliku >>')
    obraz.save(lokalizacja)
print('.')



      
      

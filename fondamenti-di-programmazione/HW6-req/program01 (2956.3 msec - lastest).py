# -*- coding: utf-8 -*-
''' 
Il sindaco si una città deve pianificare un nuovo quartiere.  Voi fate
parte dello studio di architetti che deve progettare il quartiere.  Vi
viene fornito un file che contiene divisi in righe, le informazioni
che descrivono in pianta le fasce East-West (E-W) di palazzi, ciascuno
descritto da larghezza, altezza, colore da usare in pianta.

I palazzi devono essere disposti in pianta rettangolare
in modo che:
  - tutto intorno al quartiere ci sia una strada di larghezza minima
    indicata.
  - in direzione E-W (orizzontale) ci siano le strade principali,
    dritte e della stessa larghezza minima, a separare una fascia di
    palazzi E-W dalla successiva.  Ciascuna fascia E-W di palazzi può
    contenere un numero variabile di palazzi.  Se una fascia contiene
    un solo palazzo verrà disposto al centro della fascia.
  - in direzione North-South (N-S), tra ciascuna coppia di palazzi
    consecutivi, ci dev'essere almeno lo spazio per una strada
    secondaria, della stessa larghezza minima delle altre.

Vi viene chiesto di calcolare la dimensione minima dell'appezzamento
che conterrà i palazzi.  Ed inoltre di costruire la mappa che li
mostra in pianta.

Il vostro studio di architetti ha deciso di disporre i palazzi in modo
che siano **equispaziati** in direzione E-W, e di fare in modo che
ciascuna fascia E-W di palazzi sia distante dalla seguente dello
spazio minimo necessario alle strade principali.

Per rendere il quartiere più vario, il vostro studio ha deciso che i
palazzi, invece di essere allineati con il bordo delle strade
principali, devono avere se possibile un giardino davanti (a S) ed uno
dietro (a N) di uguale profondità.  Allo stesso modo, dove possibile,
lo spazio tra le strade secondarie ed i palazzi deve essere
distribuito uniformemente in modo che tutti possano avere un giardino
ad E ed uno a W di uguali dimensioni.  Solo i palazzi che si
affacciano sulle strade sul lato sinistro e destro della mappa non
hanno giardino su quel lato.

Vi viene fornito un file txt che contiene i dati che indicano quali
palazzi mettere in mappa.  Il file contiene su ciascuna riga, seguiti
da 1 virgola e/o 0 o più spazi o tab, gruppi di 5 valori interi che
rappresentano per ciascun palazzo:
  - larghezza
  - altezza
  - canale R del colore
  - canale G del colore
  - canale B del colore

Ciascuna riga contiene almeno un gruppo di 5 interi positivi relativi
ad un palazzo da disegnare. Per ciascun palazzo dovete disegnare un
rettangolo del colore indicato e di dimensioni indicate

Realizzate la funzione ex(file_dati, file_png, spaziatura) che:
  - legge i dati dal file file_dati
  - costruisce una immagine in formato PNG della mappa e la salva nel
    file file_png
  - ritorna le dimensioni larghezza,altezza dell'immagine della mappa

La mappa deve avere sfondo nero e visualizzare tutti i palazzi come segue:
  - l'argomento spaziatura indica il numero di pixel da usare per lo
    spazio necessario alle strade esterne, principali e secondarie,
    ovvero la spaziatura minima in orizzontale tra i rettangoli ed in
    verticale tra le righe di palazzi
  - ciascun palazzo è rappresentato da un rettangolo descritto da una
    quintupla del file
  - i palazzi descritti su ciascuna riga del file devono essere
    disegnati, centrati verticalmente, su una fascia in direzione
    E-W della mappa
  - i palazzi della stessa fascia devono essere equidistanti
    orizzontalmente l'uno dall'altro con una **distanza minima di
    'spaziatura' pixel tra un palazzo ed il seguente** in modo che tutti
    i primi palazzi si trovino sul bordo della strada verticale di
    sinistra e tutti gli ultimi palazzi di trovino sul bordo della
    strada di destra
    NOTA se la fascia contiene un solo palazzo dovrà essere disegnato
    centrato in orizzontale
  - ciascuna fascia di palazzi si trova ad una distanza minima in
    verticale dalla seguente per far spazio alla strada principale
    NOTE la distanza in verticale va calcolata tra i due palazzi più
    alti delle due fasce consecutive. 
    Il palazzo più grosso della prima riga si trova appoggiato al
    bordo della strada principale E-W superiore. 
    Il palazzo più grosso dell'ultima riga si trova appoggiato al
    bordo della strada principale E-W inferiore 
  - l'immagine ha le dimensioni minime possibili, quindi:
     - esiste almeno un palazzo della prima/ultima fascia a
       'spaziatura' pixel dal bordo superiore/inferiore
     - esiste almeno una fascia che ha il primo ed ultimo palazzo a
       'spaziatura' pixel dal bordo sinistro/destro
     - esiste almeno una fascia che non ha giardini ad E ed O

    NOTA: nel disegnare i palazzi potete assumere che le coordinate
        saranno sempre intere (se non lo sono avete fatto un errore).
    NOTA: Larghezza e altezza dei rettangoli sono tutti multipli di due.
'''
  # - larghezza
  # - altezza
  # - canale R del colore
  # - canale G del colore
  # - canale B del colore

# 2956.23 msec

import images

def ex(file_dati, file_png, spaziatura):
    def get_matrice(linea):
      linea = linea.replace(' ','').replace('\t','').replace('\n','')
      linea = linea.split(',')
      linea = list(map(lambda x: int(x) if x != '' else x,linea))
      linea = [linea[i:i+5] for i in range(0,len(linea)-1 ,5)]
      return linea
    with open(file_dati , 'r', encoding='utf-8') as f:
      matrice = list(map(get_matrice,f.readlines()))

    max_sum_of_building = sum(max([building[1] for building in linea]) for linea in matrice)
    len_matrice = len(matrice)

    def get_file_sizes(matrice):
      file_width =  max([sum([palazzo[0] for palazzo in linea]) + spaziatura * (len(linea) + 1) for linea in matrice])
      file_height = max_sum_of_building + (spaziatura * (len_matrice + 1))
      return file_width,file_height
    image_size = get_file_sizes(matrice)
    image_matrix = [[(0,0,0) for _ in range(image_size[0])] for _ in range(image_size[1])]

    def main_v_division(matrice):
        return (len_matrice-1) if len_matrice > 1 else 1
    main_vertical_padding = ((image_size[1] - (spaziatura * 2)) - max_sum_of_building) // main_v_division(matrice)
    
    def c_h_division(linea):
        return (len(matrice[linea])-1) if len(matrice[linea]) > 1 else 1
    def solo_case(linea,horizontal_padding):
        return 0 if len(matrice[linea]) > 1 else (horizontal_padding // 2)
    def get_under_linea_variables(linea):
      
        horizontal_padding = ((image_size[0] - (spaziatura * 2)) - sum([building[0] for building in matrice[linea]])) // c_h_division(linea)

        horizontal_prev_building_sum = sum([max([building[1] for building in linea]) for linea in matrice[:linea]])

        linea_building_height_sum = max([building[1] for building in matrice[linea]]) 
        return horizontal_padding,horizontal_prev_building_sum,linea_building_height_sum,solo_case(linea,horizontal_padding)


    def draw_rectangles(matrice):
      for linea in range(len(matrice)):

        horizontal_padding,horizontal_prev_building_sum,linea_building_height_sum,solo_case = get_under_linea_variables(linea)

        get_linea_building_width = [matrice[linea][x][0] for x in range(len(matrice[linea]))]

        for building in range(len(matrice[linea])):

          building_width = matrice[linea][building][0]
          building_height = matrice[linea][building][1]

          sub_vertical_padding = (linea_building_height_sum - building_height) // 2

          r,g,b = matrice[linea][building][2],matrice[linea][building][3],matrice[linea][building][4]

          horizontal_coordinates = spaziatura+sub_vertical_padding+main_vertical_padding*linea+horizontal_prev_building_sum
          vertical_coordinates = spaziatura+horizontal_padding*building+sum(get_linea_building_width[:building])+solo_case

          draw_rect(building_width,building_height,horizontal_coordinates,vertical_coordinates,r,g,b)
          
    
    def draw_rect(building_width,building_height,horizontal_coordinates,vertical_coordinates,r,g,b):
        for i in range(building_width):
            for j in range(building_height):
              image_matrix[j+horizontal_coordinates][i+vertical_coordinates] = (r,g,b)
    draw_rectangles(matrice)
    images.save(image_matrix,file_png)
    return image_size[0],image_size[1]

if __name__ == '__main__':
    # ex("matrices/mat-2-97.txt", 'matrices/mat-2-97.png', 97)
    pass

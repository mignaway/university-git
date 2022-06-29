# -*- coding: utf-8 -*-
'''
Un pixel artist di fama mondiale di nome Fred Zuppa ha recentemente
prodotto diversi capolavori sottoforma di immagini quadrate raster
codificate su pixels in scala di grigi. Le immagini che ha disegnato
possono prendere valori da 0 a 255 compresi. Sfortunatamente le famose
opere sono andate perdute in quanto il suo disco rigido (ahilui!) ha
smesso di funzionare e ovviamente il buon Fred e' disperato. I
programmi per recuperarle dal filesystem non funzionano purtroppo e
cosi' Fred si affida al suo amico informatico di fiducia, il quale gli
dice:

   "Fratello, in verita' ti dico, se ti ricordi la dimensione delle
   immagini e i valori dei pixel di cui erano formate e delle
   proprieta' particolari delle tue opere, allora possiamo provare a
   scrivere un generatore ricorsivo che le produca tutte in base ai
   tuoi input, cosi' facendo possiamo provare a recuperarle!"

Il mattino seguente Fred riesce a dare le informazioni necessarie
sottoforma di:
   1. `D` parametro intero che descrive la dimensione dell'immagine
       quadrata.
   2. `colors` una lista di interi che descrive i colori delle
      immagini di Fred.  I colori di Fred sono compresi fra 0, 255.
      colors puo' essere quindi [128, 0, 255] mentre NON puo' essere
      [-100, 999]
   3. Un testo `img_properties` che descrive le proprieta' delle sue
      immagini: Il testo puo' descrivere nessuna proprita' (stringa
      vuota) oppure puo' descrivere una proprieta' che riguarda i
      pattern che le immagini devono contenere.

       Ad esempio:

       Se `img_properties` e' vuota allora le immagini non devono soddisfare
       nessuna proprieta'. Viceversa se `img_properties` e' uguale a
       'pattern_{type}_' allora signifca che le immagini devono
       mostrare il pattern di tipo `type` specificato nella stringa.
       Il pattern puo' essere di un solo tipo.

       I tipi di pattern possibili sono i quattro seguenti:
          a) 'pattern_diff_': se presente indica che presa
          arbitrariamente nelle immagini di Fred una sottoimmagine
          di dimensione uguale a 2x2, questa sottoimmagine deve avere i
          pixel di colore tutti diversi.

                 valid        not valid
            |  96 | 255 |   |   0 | 255 |
            | 128 |   0 |   | 255 |  96 |


          b) 'pattern_cross_': se presente indica che presa
          arbitrariamente nelle immagini di Fred una sottoimmagine
          di dimensione uguale a 2x2, questa sottoimmagine deve
          avere i pixel sulla diagonale uguali fra loro e i pixel
          sulla antidiagonale uguale fra loro ma pixel delle due
          diagonali devono essere diverse.

               valid          not valid     not valid
            |  96 | 255 |   |  0 | 255 |   | 61 | 61 |
            | 255 |  96 |   | 96 |   0 |   | 61 | 61 |

          c) 'pattern_hrect_': se presente indica che presa
          arbitrariamente nelle immagini di Fred una sottoimmagine di
          dimensione 2x2, questa sottoimmagine deve avere i pixel
          sulle righe tutti uguali ma righe adiacenti di colore
          diverso.

                 valid       not valid        not valid
            |   0 |   0 |   | 255 | 255 |    | 43 | 43 |
            | 128 | 128 |   | 0   | 255 |    | 43 | 43 |

          d) 'pattern_vrect_': se presente indica che presa
          arbitrariamente nelle immagini di Fred una sottoimmagine di
          dimensione 2x2, questa sottoimmagine deve avere i pixel
          sulle colonne tutti uguali ma colonne adiacenti di colore
          diverso.

                valid         not  valid    not valid
             | 0 | 255 |     | 0  | 0  |    | 22 | 22 |
             | 0 | 255 |     | 0  | 255|    | 22 | 22 |

Implementare la funzione ricorsiva o che usa metodi ricorsivi:
  
      images = ex(colors, D, img_properties)

che prende in ingresso la lista di colori `colors`, la dimensione
delle immagini `D` e una stringa `img_properties` che ne descrive le
proprieta' e generi ricorsivamente tutte le immagini seguendo le
proprieta' suddette.  La funzione deve restituire l'elenco di tutte le
immagini come una lista di immagini.  Ciascuna immagine e' una tupla di
tuple dove ogni intensita' di grigio e' un intero.
// IMPORTANT L'ordine in cui si generano le immagini non conta.

     Esempio: immagine 2x2 di zeri (tutto nero) e':
        img = ( (0, 0), (0, 0), )


Il timeout per ciascun test è di 1 secondo.

***
E' fortemente consigliato di modellare il problema come un albero di
gioco, cercando di propagare le solo le "mosse" necessarie nella
ricorsione e quindi nella costruzione della soluzione in maniera
efficiente; oppure, in maniera alternativa, cercate di "potare" l'albero di
gioco il prima possibile.
***

Potete visualizzare tutte le immagini da generare invocando

     python test_01.py data/images_data_15.json

questo salva su disco tutte le immagini attese del test 15 e crea
un file HTML di nome `images_data_15.html` nella directory radice
del HW con cui e' possibile vedere le immagini aprendo il file html
con browser web.
'''
'''

APPUNTI PERSONALI

// Ricorsione funzionamento
# []
# [0],[255]
# [0,0],[0,255],[255,0],[255,255] 
# [0,0,0],[0,0,255],[0,255,0],[0,255,255],[255,0,0],[255,0,255],[255,255,0],[255,255,255]
# ... | Per ogni linea aggiungi i colori

'''
def normalize_combination_default(combination,d):
   final = []
   for linea in combination:
       final.append(tuple([tuple(linea[i:i+d]) for i in range(0, len(linea), d)]))
   return final
def normalize_combination_vrect(combination,d):
   return [tuple([tuple(linea)]*d) for linea in combination]
def normalize_combination_hrect(combination, d):
   return [tuple([tuple([x]*d) for x in linea]) for linea in combination]

def generate_combination_default(colori, d):
   if d == 0:
      return [[]]
   final = []
   for linea in generate_combination_default(colori, d-1):
      for colore in colori:
         final.append(linea + [colore])
   return final
def normalize_combination_cross(combination, d):
   final = []
   for linea in combination:
      if d % 2 == 0:
         normale = linea * int(d/2)
         invertito = linea[::-1] * int(d/2)
         final.append(tuple([tuple(normale if i % 2 == 0 else invertito) for i in range(d)]))
      else:
         normale = linea * int((d-1)/2)
         invertito = linea[::-1] * int((d-1)/2)
         final.append(tuple([tuple(normale + [normale[0]] if i % 2 == 0 else invertito + [invertito[0]]) for i in range(d)]))
   return final

def generate_combination_vrect(colori, d):
   if d == 0:
      return [[]]
   final = []
   for linea in generate_combination_vrect(colori, d-1):
      for colore in colori:
         pippo = linea + [colore]
         if len(pippo[-2:]) == len(set(pippo[-2:])):
            final.append(pippo)
   return final
def generate_combination_diff(colori,d,p):
   if d == 0:
      return [[]]
   final = []
   for linea in generate_combination_diff(colori, d-1, p):
      for colore in colori:
         pippo = linea + [colore]
         if len(pippo) >= p:
            start_index = p * (int(len(pippo) / p)-1)
            if len(pippo[start_index+p:start_index+p+2]) == 2 or len(pippo[start_index+p:start_index+p+2]) == 0:
               bottom_index = len(pippo)-2-p
               pippo_ultra = pippo[bottom_index:bottom_index+2] + pippo[-2:]
               if len(pippo_ultra) == len(set(pippo_ultra)):
                  final.append(pippo)
            else:
               final.append(pippo)
         else:
            if len(pippo[-2:]) == len(set(pippo[-2:])):
               final.append(pippo)
   return final


def ex(colors, D, img_properties):
   if not img_properties: return normalize_combination_default(generate_combination_default(colors, D*D),D)
   elif img_properties == 'pattern_vrect_': return normalize_combination_vrect(generate_combination_vrect(colors, D),D)
   elif img_properties == 'pattern_hrect_': return normalize_combination_hrect(generate_combination_vrect(colors, D),D)
   elif img_properties == 'pattern_cross_': return normalize_combination_cross(generate_combination_vrect(colors, 2), D)
   elif img_properties == 'pattern_diff_': return normalize_combination_default(generate_combination_diff(colors, D*D,D),D)
   
if __name__ == '__main__':
   pass

# (303ms - 7c) on VM

import pronouncing
import math

def PoemSync(inputfilename, outputfilename, tau):
    def line_to_matrix(lista):
        new_lista = []
        for x in lista:
            parola = "".join(map(lambda x: x if x.isalpha() else ' ', x))
            parola = parola.split()
            for j in parola:
                if pronouncing.phones_for_word(j):
                    get_stresses = pronouncing.stresses(pronouncing.phones_for_word(j)[0])
                    if len(get_stresses) > 1:
                        new_lista.extend(map(lambda x: 1 if int(x) == 1 else 0, list(get_stresses)))
                    else:
                        new_lista.extend([int(get_stresses)])
                else:
                    # new_lista.extend([0 for i in range(len(j)//2)])
                    new_lista.extend([0] *(len(j)//2))
                new_lista.append(0)
        return new_lista
    
    file_text = list(map(lambda x: x.split(), open(inputfilename, encoding="utf-8").readlines()))
    matrix = list(map(line_to_matrix, file_text))
    matrix = list(filter(None, matrix))
    max_file_text = len(max(matrix,key=len))
    
    def align_left(lista):
        lista.extend([0] * (max_file_text - len(lista)))
        return lista
    matrix = list(map(align_left,matrix))
    
    
    
    with open(outputfilename,'w',encoding="utf-8") as f:
        for element in matrix:
            f.write("".join(map(str,element)) + "\n")
    def get_ab(lista1,lista2):
        return sum([1 for i, v in enumerate(lista2) if v == 1 and 1 in lista1[(i-tau) if (i-tau) > 0 else 0:i+1]])
    def get_ba(lista1,lista2):
        return sum([1 for i, v in enumerate(lista1) if v == 1 and 1 in lista2[(i-tau) if (i-tau) > 0 else 0:i+1]])
    def sync_matrix(lista1,lista2):
        m_a, m_b = lista1.count(1), lista2.count(1)
        if m_a == 0 or m_b == 0:
            return 0
        sync = (0.5 * (get_ba(lista1,lista2)+get_ab(lista1,lista2)))/math.sqrt(m_a*m_b)
        return sync
    matrix_sync = [sync_matrix(matrix[i], matrix[j]) for i in range(len(matrix)) for j in range(i+1, len(matrix))]
    return round(sum(matrix_sync)/len(matrix_sync),6)


if __name__ == "__main__":
    # print(PoemSync("poems/text04.txt", "poems/text04.out.txt", 2))
    pass
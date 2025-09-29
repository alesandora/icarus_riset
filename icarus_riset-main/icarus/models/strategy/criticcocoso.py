import copy
import pandas as pd
import numpy as np

def criticcocoso(mut):
    l = 0.5 # nilai lambda

    # 1. Data Awal
    matrix = copy.deepcopy(mut)
    mata = []
    matkey = []

    for x in matrix:
        mata.append(matrix[x])
        matkey.append(x)

    matat = [[0 for i in range(len(mata))]for j in range(len(mata[0]))] #matriks transpose
    for x in range(len(mata)):
        for y in range(len(mata[0])):
            matat[y][x] = mata[x][y]

    inddel = []
    for x in range(len(matat)):
        if max(matat[x]) == min(matat[x]):
            inddel.append(x)
    
    if len(inddel) > 0:
        for x in reversed(inddel):
            matat.pop(x)

        mata = [[0 for i in range(len(matat))]for j in range(len(matat[0]))]
        for x in range(len(matat)):
            for y in range(len(matat[0])):
                mata[y][x] = matat[x][y]

    # 2. Tranformasi
    mattran = [[0 for i in range(len(mata))]for j in range(len(mata[0]))] #matriks transformasi
    for x in range(len(matat)):
        for y in range(len(matat[0])):
            mattran[x][y] = (matat[x][y] - min(matat[x]))/(max(matat[x])-min(matat[x]))

    # 3. Correlation Matrix
    dataframe = pd.DataFrame(mata)
    matcorr = dataframe.corr()
    matcorr = matcorr.values.tolist() #matriks korelasi

    # 4. Conflict Matrix
    confmat = [[0 for i in range(len(matcorr))]for j in range(len(matcorr[0]))] #conflictmatrix
    for x in range(len(confmat)):
        for y in range(len(confmat[0])):
            confmat[x][y] = 1-matcorr[x][y]
    
    # 5. CJ: Amount of info
    stddev = [0 for x in range(len(mata[0]))]
    for x in range(len(stddev)):
        stddev[x] = np.std(mattran[x])

    totrjk = [0 for x in range(len(mata[0]))]
    for x in range(len(totrjk)):
        totrjk[x] = sum(confmat[x])
    
    cj = [0 for x in range(len(mata[0]))]
    for x in range(len(cj)):
        cj[x] = stddev[x] * totrjk[x]

    totcj = sum(cj)

    # 6. wj : bobot
    wj = [0 for x in range(len(mata[0]))]
    for x in range(len(wj)):
        if totcj != 0:
            wj[x] = cj[x]/totcj
        else:
            wj[x] = 1/len(wj)
    
    # 3.) Menentukan total dari perbandingan urutan bobot dengan keseluruhan bobot,
    si = [0 for x in range(len(mata))]
    for x in range(len(mattran[0])):
        temp = 0
        for y in range(len((mattran))):
            temp += wj[y]*mattran[y][x]
        if temp != 0:
            si[x] = temp
        else:
            si[x] = 0.00001

    pi = [0 for x in range(len(mata))]
    for x in range(len(mattran[0])):
        temp = 0
        for y in range(len((mattran))):
            temp += mattran[y][x] ** wj[y]
        if temp != 0:
            pi[x] = temp
        else:
            pi[x] = 0.00001
    
    # 4.) Bobot relatif dari alternatif menggunakan strategi agregasi perhitungan
    kia = [0 for x in range(len(mata))]
    for x in range(len(kia)):
        kia[x] = (pi[x]+si[x])/(sum(pi)+sum(si))

    kib = [0 for x in range(len(mata))]
    for x in range(len(kib)):
        kib[x] = si[x]/min(si) + pi[x]/min(pi)

    kic = [0 for x in range(len(mata))]
    for x in range(len(kic)):
        kic[x] = (l*si[x] + (1-l)*pi[x]) / (l*max(si)+(1-l)*max(pi))

    # 5.) Nilai akhir rangking dari alternatif
    ki = [0 for x in range(len(mata))]
    for x in range(len(ki)):
        ki[x] = (kia[x]*kib[x]*kic[x])**(1/3) + (1/3)*(kia[x]+kib[x]+kic[x])

    return matkey[ki.index(max(ki))]

#tesdict = {
#    23 : [8, 9, 9.5, 0],
#    31 : [9, 9, 9.5, 0],
#    85 : [9, 7, 9.5, 0],
#   21 : [8, 5, 7, 0],
#    59 : [8, 9, 8, 9.5]
#}

#hasilcriticcocoso = criticcocoso(tesdict)

#print(f"Node cache berdasarkan hasil critic-cocoso adalah : {hasilcriticcocoso}")
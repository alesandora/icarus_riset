import copy
from numpy import log as ln

def ewmtopsis(mut):             #ewm + topsis Standar
    #Membuat matriks utama
    mata = []
    matkey = []
    for x in mut:
        mata.append(mut[x])
        matkey.append(x)

    matat = [[0 for i in range(len(mata))]for j in range(len(mata[0]))] #matriks transpose
    for x in range(len(mata)):
        for y in range(len(mata[0])):
            matat[y][x] = mata[x][y]

    for x in range(len(matat)):
        if sum(matat[x]) == 0:
            matat[x] = [1 for i in range(len(matat[x]))]
    
    for x in range(len(matat)):
        for y in range(len(matat[0])):
            mata[y][x] = matat[x][y]

    #2) Matriks Ternormalisasi / Standarisasi
    #Matrik ternormalisasi = akar dari hasil pangkat nilai pada setiap kriteria (x=√C^2)
    mt = [0 for i in range(len(mata[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += mata[y][x]**2
    
    for x in range(len(mt)):
        mt[x] = mt[x]**0.5

    #Rating Kinerja Ternormalisasi (rij/zij)
    #Normalisasi R = data nilai / matriks ternormalisasi
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mata[y][x] /= mt[x]
    
    #3) Pembobotan Kriteria
    #Bobot (W)
    mt = [0 for i in range(len(mata[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += mata[y][x]
    
    #Rating Kinerja Ternormalisasi (pij)
    #Normalisasi R = data nilai / matriks ternormalisasi
    matb = copy.deepcopy(mata)
    for x in range(len(matb[0])):
        for y in range(len(matb)):
            matb[y][x] /= mt[x]
    
    #hitung E1 E2 E3 E4
    mt = [0 for i in range(len(matb[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += matb[y][x]*ln(matb[y][x])

    #hitung e1 e2 e3 e4
    for x in range(len(mt)):
        mt[x] *= (-ln(1/len(matb)))

    #hitung w1 w2 w3 w4
    w = [0 for i in range(len(mt))]
    for x in range(len(w)):
        w[x] = (1-mt[x]) / (len(matb[0])-sum(mt))
    
    #MASUK KE TOPSIS

    #Rating Bobot Ternormalisasi(yij)
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mata[y][x] *= w[x]
    
    #4) matrik solusi ideal positif dan negatif 
    #A+ / Y+= Nilai MAX dari hasil nilai kriteria terbobot (MAX=nilai terbesar)
    #A-/Y- = nilai MIN dari hasil nilai kriteria terbobot (MIN=nilai terkecil)
    matat = [[0 for i in range(len(mata))]for j in range(len(mata[0]))] #matriks transpose
    for x in range(len(mata)):
        for y in range(len(mata[0])):
            matat[y][x] = mata[x][y]

    apos = [0 for i in range(len(matat))]
    for x in range(len(matat)):
        apos[x] = max(matat[x])

    aneg = [0 for i in range(len(matat))]
    for x in range(len(matat)):
        aneg[x] = min(matat[x])

    #jarak antara nilai setiap alternatif dengan matriks solusi ideal positif & matriks solusi ideal negatif
    #Positif= hasil akar dari hasil  (A+ dikurangi data terbobot) pangkat 2
    #Negatif= hasil akar dari hasil  (A- dikurangi data terbobot) pangkat 2
    dipos = [0 for i in range(len(mata))]
    
    for x in range(len(mata)):
        tempres = 0
        for y in range(len(mata[0])):
            tempres += (apos[y]-mata[x][y])**2
        dipos[x] = tempres**0.5

    dineg = [0 for i in range(len(mata))]
    
    for x in range(len(mata)):
        tempres = 0
        for y in range(len(mata[0])):
            tempres += (aneg[y]-mata[x][y])**2
        dineg[x] = tempres**0.5

    #5) NILAI PRFERENSI DARI SETIAP KRITERIA
    #Hasil akhir = solusi ideal negatif (D-) / jumlah solusi ideal positif dan negatif (D+ + D-)
    #Vi /Si = D- / (D+ + D-)

    s = [0 for i in range(len(mata))]
    for x in range(len(s)):
        s[x] = dineg[x] / (dineg[x]+dipos[x])

    return matkey[s.index(max(s))]

def ewmtopsis_v1(mut):             #ewm + topsis pij = 0 ==> ej = 0
    #Membuat matriks utama
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

    for x in range(len(matat)):
        if sum(matat[x]) == 0:
            matat[x] = [1 for i in range(len(matat[x]))]
    
    for x in range(len(matat)):
        for y in range(len(matat[0])):
            mata[y][x] = matat[x][y]

    #2) Matriks Ternormalisasi / Standarisasi
    #Matrik ternormalisasi = akar dari hasil pangkat nilai pada setiap kriteria (x=√C^2)
    mt = [0 for i in range(len(mata[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += mata[y][x]**2
    
    for x in range(len(mt)):
        mt[x] = mt[x]**0.5

    #Rating Kinerja Ternormalisasi (rij/zij)
    #Normalisasi R = data nilai / matriks ternormalisasi
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mata[y][x] /= mt[x]
    
    #3) Pembobotan Kriteria
    #Bobot (W)
    mt = [0 for i in range(len(mata[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += mata[y][x]
    
    #Rating Kinerja Ternormalisasi (pij)
    #Normalisasi R = data nilai / matriks ternormalisasi
    matb = copy.deepcopy(mata)
    for x in range(len(matb[0])):
        for y in range(len(matb)):
            matb[y][x] /= mt[x]
    
    #hitung E1 E2 E3 E4
    mt = [0 for i in range(len(matb[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            if matb[y][x] == 0:
                mt[x] = 0
                break
            else:
                mt[x] += matb[y][x]*ln(matb[y][x])

    #hitung e1 e2 e3 e4
    for x in range(len(mt)):
        mt[x] *= (-ln(1/len(matb)))

    #hitung w1 w2 w3 w4
    w = [0 for i in range(len(mt))]
    for x in range(len(w)):
        w[x] = (1-mt[x]) / (len(matb[0])-sum(mt))
    
    #MASUK KE TOPSIS

    #Rating Bobot Ternormalisasi(yij)
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mata[y][x] *= w[x]
    
    #4) matrik solusi ideal positif dan negatif 
    #A+ / Y+= Nilai MAX dari hasil nilai kriteria terbobot (MAX=nilai terbesar)
    #A-/Y- = nilai MIN dari hasil nilai kriteria terbobot (MIN=nilai terkecil)
    matat = [[0 for i in range(len(mata))]for j in range(len(mata[0]))] #matriks transpose
    for x in range(len(mata)):
        for y in range(len(mata[0])):
            matat[y][x] = mata[x][y]

    apos = [0 for i in range(len(matat))]
    for x in range(len(matat)):
        apos[x] = max(matat[x])

    aneg = [0 for i in range(len(matat))]
    for x in range(len(matat)):
        aneg[x] = min(matat[x])

    #jarak antara nilai setiap alternatif dengan matriks solusi ideal positif & matriks solusi ideal negatif
    #Positif= hasil akar dari hasil  (A+ dikurangi data terbobot) pangkat 2
    #Negatif= hasil akar dari hasil  (A- dikurangi data terbobot) pangkat 2
    dipos = [0 for i in range(len(mata))]
    
    for x in range(len(mata)):
        tempres = 0
        for y in range(len(mata[0])):
            tempres += (apos[y]-mata[x][y])**2
        dipos[x] = tempres**0.5

    dineg = [0 for i in range(len(mata))]
    
    for x in range(len(mata)):
        tempres = 0
        for y in range(len(mata[0])):
            tempres += (aneg[y]-mata[x][y])**2
        dineg[x] = tempres**0.5

    #5) NILAI PRFERENSI DARI SETIAP KRITERIA
    #Hasil akhir = solusi ideal negatif (D-) / jumlah solusi ideal positif dan negatif (D+ + D-)
    #Vi /Si = D- / (D+ + D-)

    s = [0 for i in range(len(mata))]
    for x in range(len(s)):
        s[x] = dineg[x] / (dineg[x]+dipos[x])

    return matkey[s.index(max(s))]

def ewmtopsis_v2(mut):             #ewmtopsis_v1 + standarisasi matriks
    #Membuat matriks utama
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

    for x in range(len(matat)):
        if x != 2:
            nmax = max(matat[x])
            for y in range(len(matat[0])):
                matat[x][y] = nmax - matat[x][y]
            
    for x in range(len(matat)):
        if sum(matat[x]) == 0:
            matat[x] = [1 for i in range(len(matat[x]))]
    
    for x in range(len(matat)):
        for y in range(len(matat[0])):
            mata[y][x] = matat[x][y]

    #2) Matriks Ternormalisasi / Standarisasi
    #Matrik ternormalisasi = akar dari hasil pangkat nilai pada setiap kriteria (x=√C^2)
    mt = [0 for i in range(len(mata[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += mata[y][x]**2
    
    for x in range(len(mt)):
        mt[x] = mt[x]**0.5

    #Rating Kinerja Ternormalisasi (rij/zij)
    #Normalisasi R = data nilai / matriks ternormalisasi
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mata[y][x] /= mt[x]
    
    #3) Pembobotan Kriteria
    #Bobot (W)
    mt = [0 for i in range(len(mata[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += mata[y][x]
    
    #Rating Kinerja Ternormalisasi (pij)
    #Normalisasi R = data nilai / matriks ternormalisasi
    matb = copy.deepcopy(mata)
    for x in range(len(matb[0])):
        for y in range(len(matb)):
            matb[y][x] /= mt[x]
    
    #hitung E1 E2 E3 E4
    mt = [0 for i in range(len(matb[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            if matb[y][x] == 0:
                mt[x] = 0
                break
            else:
                mt[x] += matb[y][x]*ln(matb[y][x])

    #hitung e1 e2 e3 e4
    for x in range(len(mt)):
        mt[x] *= (-ln(1/len(matb)))

    #hitung w1 w2 w3 w4
    w = [0 for i in range(len(mt))]
    for x in range(len(w)):
        w[x] = (1-mt[x]) / (len(matb[0])-sum(mt))
    
    #MASUK KE TOPSIS

    #Rating Bobot Ternormalisasi(yij)
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mata[y][x] *= w[x]
    
    #4) matrik solusi ideal positif dan negatif 
    #A+ / Y+= Nilai MAX dari hasil nilai kriteria terbobot (MAX=nilai terbesar)
    #A-/Y- = nilai MIN dari hasil nilai kriteria terbobot (MIN=nilai terkecil)
    matat = [[0 for i in range(len(mata))]for j in range(len(mata[0]))] #matriks transpose
    for x in range(len(mata)):
        for y in range(len(mata[0])):
            matat[y][x] = mata[x][y]

    apos = [0 for i in range(len(matat))]
    for x in range(len(matat)):
        apos[x] = max(matat[x])

    aneg = [0 for i in range(len(matat))]
    for x in range(len(matat)):
        aneg[x] = min(matat[x])

    #jarak antara nilai setiap alternatif dengan matriks solusi ideal positif & matriks solusi ideal negatif
    #Positif= hasil akar dari hasil  (A+ dikurangi data terbobot) pangkat 2
    #Negatif= hasil akar dari hasil  (A- dikurangi data terbobot) pangkat 2
    dipos = [0 for i in range(len(mata))]
    
    for x in range(len(mata)):
        tempres = 0
        for y in range(len(mata[0])):
            tempres += (apos[y]-mata[x][y])**2
        dipos[x] = tempres**0.5

    dineg = [0 for i in range(len(mata))]
    
    for x in range(len(mata)):
        tempres = 0
        for y in range(len(mata[0])):
            tempres += (aneg[y]-mata[x][y])**2
        dineg[x] = tempres**0.5

    #5) NILAI PRFERENSI DARI SETIAP KRITERIA
    #Hasil akhir = solusi ideal negatif (D-) / jumlah solusi ideal positif dan negatif (D+ + D-)
    #Vi /Si = D- / (D+ + D-)

    s = [0 for i in range(len(mata))]
    for x in range(len(s)):
        s[x] = dineg[x] / (dineg[x]+dipos[x])

    return matkey[s.index(max(s))]

def ewmtopsis_v3(mut):             #standarisasi matriks , nilai 0 == 0.0001
    #Membuat matriks utama
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

    for x in range(len(matat)):
        if x != 2:
            nmax = max(matat[x])
            for y in range(len(matat[0])):
                matat[x][y] = nmax - matat[x][y]
            
    for x in range(len(matat)):
        for y in range(len(matat[0])):
            if matat[x][y] == 0:
                matat[x][y] = 0.0001
    
    for x in range(len(matat)):
        for y in range(len(matat[0])):
            mata[y][x] = matat[x][y]

    #2) Matriks Ternormalisasi / Standarisasi
    #Matrik ternormalisasi = akar dari hasil pangkat nilai pada setiap kriteria (x=√C^2)
    mt = [0 for i in range(len(mata[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += mata[y][x]**2
    
    for x in range(len(mt)):
        mt[x] = mt[x]**0.5

    #Rating Kinerja Ternormalisasi (rij/zij)
    #Normalisasi R = data nilai / matriks ternormalisasi
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mata[y][x] /= mt[x]
    
    #3) Pembobotan Kriteria
    #Bobot (W)
    mt = [0 for i in range(len(mata[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += mata[y][x]
    
    #Rating Kinerja Ternormalisasi (pij)
    #Normalisasi R = data nilai / matriks ternormalisasi
    matb = copy.deepcopy(mata)
    for x in range(len(matb[0])):
        for y in range(len(matb)):
            matb[y][x] /= mt[x]
    
    #hitung E1 E2 E3 E4
    mt = [0 for i in range(len(matb[0]))]
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mt[x] += matb[y][x]*ln(matb[y][x])

    #hitung e1 e2 e3 e4
    for x in range(len(mt)):
        mt[x] *= (-ln(1/len(matb)))

    #hitung w1 w2 w3 w4
    w = [0 for i in range(len(mt))]
    for x in range(len(w)):
        w[x] = (1-mt[x]) / (len(matb[0])-sum(mt))
    
    #MASUK KE TOPSIS

    #Rating Bobot Ternormalisasi(yij)
    for x in range(len(mata[0])):
        for y in range(len(mata)):
            mata[y][x] *= w[x]
    
    #4) matrik solusi ideal positif dan negatif 
    #A+ / Y+= Nilai MAX dari hasil nilai kriteria terbobot (MAX=nilai terbesar)
    #A-/Y- = nilai MIN dari hasil nilai kriteria terbobot (MIN=nilai terkecil)
    matat = [[0 for i in range(len(mata))]for j in range(len(mata[0]))] #matriks transpose
    for x in range(len(mata)):
        for y in range(len(mata[0])):
            matat[y][x] = mata[x][y]

    apos = [0 for i in range(len(matat))]
    for x in range(len(matat)):
        apos[x] = max(matat[x])

    aneg = [0 for i in range(len(matat))]
    for x in range(len(matat)):
        aneg[x] = min(matat[x])

    #jarak antara nilai setiap alternatif dengan matriks solusi ideal positif & matriks solusi ideal negatif
    #Positif= hasil akar dari hasil  (A+ dikurangi data terbobot) pangkat 2
    #Negatif= hasil akar dari hasil  (A- dikurangi data terbobot) pangkat 2
    dipos = [0 for i in range(len(mata))]
    
    for x in range(len(mata)):
        tempres = 0
        for y in range(len(mata[0])):
            tempres += (apos[y]-mata[x][y])**2
        dipos[x] = tempres**0.5

    dineg = [0 for i in range(len(mata))]
    
    for x in range(len(mata)):
        tempres = 0
        for y in range(len(mata[0])):
            tempres += (aneg[y]-mata[x][y])**2
        dineg[x] = tempres**0.5

    #5) NILAI PRFERENSI DARI SETIAP KRITERIA
    #Hasil akhir = solusi ideal negatif (D-) / jumlah solusi ideal positif dan negatif (D+ + D-)
    #Vi /Si = D- / (D+ + D-)

    s = [0 for i in range(len(mata))]
    for x in range(len(s)):
        s[x] = dineg[x] / (dineg[x]+dipos[x])

    return matkey[s.index(max(s))]
    
#tesdict = {
#    23 : [0.432, 78, 569, 2],
#    31 : [0.312, 65, 487, 3],
#    85 : [0.215, 45, 541, 4],
#    21 : [0.274, 54, 487, 5],
#    59 : [0.346, 34, 400, 6]
#}

#Daftar fungsi
# ewmtopsis ==> ewm topsis standar
# ewmtopsis_v1 ==> pij = 0 --> ej = 0
# ewmtopsis_v2 ==> ewmtopsis_v1 + standarisasi matriks
# ewmtopsis_v3 ==> standarisasi matriks , nilai 0 == 0.0001

#hasiltopsis = ewmtopsis_v1(tesdict)

#print(f"Node cache berdasarkan hasil ewm-topsis adalah : {hasiltopsis}")
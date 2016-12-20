__author__ = "Arno Kender (163256IATM)"
__version__ = "2.0"
__email__ = "arno.kender@gmail.com"

from PIL import Image
import numpy as np
from math import pi, cos, sqrt, log10
import sys

# ::: DCT kooder ja dekooder :::

# ::: Parameetrid :::
blocksize = 8

# ::: Faili lugemine :::
filename = 'lena512.bmp'
bmpimg = Image.open(filename, 'r')


def getrecoveredcos(Q, bs):
    # Q - quarter matrix
    # bs - blocksize
    al, aw = np.shape(Q)
    B = np.zeros((int(al * 2), int(aw * 2)))  # recovered quarters
    for M in range(int(al * 2 / bs)):
        for N in range(int(aw * 2 / bs)):
            q = np.zeros((bs, bs))
            x1 = int(M * bs / 2)
            x2 = int((M + 1) * bs / 2)
            y1 = int(N * bs / 2)
            y2 = int((N + 1) * bs / 2)
            q[0:int(bs / 2), 0:int(bs / 2)] = Q[x1:x2, y1:y2]
            x1 = int(M * bs)
            x2 = int((M + 1) * bs)
            y1 = int(N * bs)
            y2 = int((N + 1) * bs)
            B[x1:x2, y1:y2] = q
    return B


def getquartercos(B, bs):
    # B -
    # bs - blocksize
    al, aw = np.shape(B)
    Q = np.zeros((int(al / 2), int(aw / 2)))  # quarters
    for M in range(int(al / bs)):
        for N in range(int(aw / bs)):
            x1 = int(M * bs)
            x2 = int((M + 1) * bs)
            y1 = int(N * bs)
            y2 = int((N + 1) * bs)
            whole = B[x1:x2, y1:y2]
            x1 = int(M * bs / 2)
            x2 = int((M + 1) * bs / 2)
            y1 = int(N * bs / 2)
            y2 = int((N + 1) * bs / 2)
            Q[x1:x2, y1:y2] = whole[0:int(bs / 2), 0:int(bs / 2)]
    return Q


def getalphas(al):
    # al - array length
    alphas = [1 / sqrt(al)]
    for i in range(1, al):
        alphas.append(sqrt(2 / al))
    return alphas


def getdctsum(Ab, p, q):
    # Ab - block of A
    # p, q - pixel index
    M, N = np.shape(Ab)
    suml = []  # cos transform list
    for m in range(M):
        for n in range(N):
            suml.append(Ab[m, n] * cos(pi * (2 * m + 1) * p / (2 * M)) * cos(pi * (2 * n + 1) * q / (2 * N)))
    return sum(suml)


def getcos(Ab):
    # Ab - block of A
    al, aw = np.shape(Ab)
    alphas = getalphas(al)
    Bb = np.zeros((al, aw))  # block of B
    for p in range(al):
        for q in range(aw):
            Bb[p, q] = alphas[p] * alphas[q] * getdctsum(Ab, p, q)
    return Bb


def getidctsum(Bb, m, n):
    # Bb - block of B
    # m, n - pixel index
    M, N = np.shape(Bb)
    alphas = getalphas(8)
    suml = []  # cos transform list
    for p in range(M):
        for q in range(N):
            suml.append(alphas[p] * alphas[q] * Bb[p, q] * cos(pi * (2 * m + 1) * p / (2 * M)) * cos(pi * (2 * n + 1) * q / (2 * N)))
    return sum(suml)


def geticos(Bb):
    # Bb -
    al, aw = np.shape(Bb)
    Ab = np.zeros((al, aw))  # block of A
    for m in range(al):
        for n in range(aw):
            Ab[m, n] = getidctsum(Bb, m, n)
    return Ab


def dct2(A, bs):
    # A - original matrix
    # bs - blocksize
    al, aw = np.shape(A)  # array length, width
    B = np.zeros((al, aw))
    for M in range(int(al / bs)):
        for N in range(int(aw / bs)):
            sys.stdout.write('\rdct2() rida: %s, veerg: %s' % (str(M + 1), str(N + 1)))
            x1 = int(M * bs)
            x2 = int((M + 1) * bs)
            y1 = int(N * bs)
            y2 = int((N + 1) * bs)
            B[x1:x2, y1:y2] = getcos(A[x1:x2, y1:y2])
    print()
    return B


def idct2(B, bs):
    # B -
    # bs - blocksize
    al, aw = np.shape(B)
    A = np.zeros((al, aw))  # recovered matrix
    for M in range(int(al / bs)):
        for N in range(int(aw / bs)):
            sys.stdout.write('\ridct2() rida: %s, veerg: %s' % (str(M + 1), str(N + 1)))
            x1 = int(M * bs)
            x2 = int((M + 1) * bs)
            y1 = int(N * bs)
            y2 = int((N + 1) * bs)
            A[x1:x2, y1:y2] = geticos(B[x1:x2, y1:y2])
    print()
    return A


def mse(A, B):
    al, aw = np.shape(A)
    li = []
    for i in range(al):
        for j in range(aw):
            li.append(pow((int(A[i, j]) - int(B[i, j])), 2))
    return sqrt(sum(li) / len(li))


def snr(A, B):
    al, aw = np.shape(A)
    s1 = 0
    s2 = 0
    for i in range(al):
        for j in range(aw):
            s1 += int(B[i, j])
            s2 += int(A[i, j])
    return 10 * log10(pow(s1, 2) / pow(s1 - s2, 2))


original = np.array(bmpimg)
cosmatrix = dct2(original, blocksize)
quartercos = getquartercos(cosmatrix, blocksize)
recoveredcos = getrecoveredcos(quartercos, blocksize)
recovered = idct2(recoveredcos, blocksize)
Image.fromarray(recovered.astype('uint8')).save('recovered.jpeg')

print('\nMSE: %s' % mse(original, recovered))
print('SNR: %s' % snr(original, recovered))
al1, aw1 = np.shape(original)
al2, aw2 = np.shape(quartercos)
print('Tihendamise efektiivsus: %s\n' % ((al1 * aw1 * blocksize) / (al2 * aw2 * blocksize)))
X = 1
Y = 1
print('Vabalt valitud bloki teisendatud maatriks:\n%s' % (str(cosmatrix[(X - 1) * blocksize:X * blocksize, (Y - 1) * blocksize:Y * blocksize])))

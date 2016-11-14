__author__ = "Arno Kender (163256IATM)"
__version__ = "1.0"
__email__ = "arno.kender@gmail.com"

import math
import wave
import struct

# ::: DPCM kooder ja dekooder :::


def getdelta(x1, bit=8):
    d = []
    for n in range(len(x1)):
        if n == 0:
            d.append(x1[n] - 0)
        else:
            d.append(x1[n] - x1[n - 1])
    return max(d) / ((math.pow(2, bit) - 2) / 2)


def getalpha():
    # return [0.6917, 0.1818, -0.1681]
    # return [2.8, -2.7, 0.9]
    return [2.8054, -2.7102, 0.9014]


def predictor(x2, alpha):
    default = [0, 0, 0]
    last3r = x2[-3:][::-1]
    for i in range(len(last3r)):
        default[i] = float(last3r[i])
    return alpha[0] * default[0] + alpha[1] * default[1] + alpha[2] * default[2]


def mse(x1, x2):
    m = []
    for n in range(len(x1)):
        m.append(math.pow(x1[n] - float(x2[n]), 2))
    return math.sqrt(sum(m) / len(m))


def snr(x1, x2):
    return 10 * math.log10(pow(sum(x1), 2) / pow(sum(x1) - sum(x2), 2))


def dpcmencode(x1, bit=8):
    p = []
    d1 = []
    k = []
    d2 = []
    x2 = []
    delta = getdelta(x1, bit)
    alpha = getalpha()
    for n in range(len(x1)):
        p.append(predictor(x2[-3:], alpha))
        d1.append(x1[n] - p[n])
        k.append(math.floor(d1[n] / delta + 0.5))
        d2.append(k[n] * delta)
        x2.append(d2[n] + p[n])
    print('DELTA: %s' % str(delta))
    print('MSE: %s' % str(mse(x1, x2)))
    print('SNR: %s' % str(snr(x1, x2)))
    return [k, delta, alpha]


def dpcmdecode(codeinfo):
    p = []
    d2 = []
    x2 = []
    for n in range(len(codeinfo[0])):
        p.append(predictor(x2[-3:], codeinfo[2]))
        d2.append(codeinfo[0][n] * codeinfo[1])
        x2.append(d2[n] + p[n])
    return [x2, p]


def wav_to_floats(wave_file):
    wav_file = wave.open(wave_file)
    astr = wav_file.readframes(wav_file.getnframes())
    list_of_floats = struct.unpack("%ih" % (wav_file.getnframes() * wav_file.getnchannels()), astr)
    list_of_floats = [float(val) / pow(2, 15) for val in list_of_floats]
    wav_file.close()
    return list_of_floats


def floats_to_wav(list_of_floats, wave_file, amp=1):
    list_of_integers = [int(float(val) * pow(2, 15)) for val in list_of_floats]
    wav_file = wave.open(wave_file, "w")
    wav_file.setparams((1, 2, 44100, len(list_of_integers), "NONE", "not compressed"))
    for val in list_of_integers:
        wav_file.writeframes(struct.pack('h', int(val * amp / 2)))
    wav_file.close()


# src = [0.9, 0.8, 0.7, 0.55, 0.1, 0.4]
src = wav_to_floats('pcm1644m.wav')

# print('Algne sisend: %s\n' % str(src))
print('Kodeerimine:')
coded = dpcmencode(src)
dstfile = open('code.txt', 'w')
dstfile.write(str(coded[0]))
dstfile.close()
print('\nDekodeerimine:')
decoded = dpcmdecode(coded)
dstfile = open('decoded.txt', 'w')
dstfile.write(str(decoded[0]))
dstfile.close()
floats_to_wav(decoded[0], 'decoded.wav')
print('\nValmis!')

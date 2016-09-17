__author__ = "Arno Kender (163256IATM)"
__version__ = "2.0"
__email__ = "arno.kender@gmail.com"

# ::: Shannoni entroopia arvutamine pildifaili naaberpikslite erinevuse alusel :::
import os.path
from PIL import Image
import math

# ::: Faili lugemine :::
filename = 'barbara512.bmp'
# filename = 'lena512.bmp'
img = Image.open(filename, 'r')
src = list(img.getdata())


# ::: Info sageduse, t6en2osuse ja entroopia arvutamine :::
def getresult(source):
    result = {'info': list(set(source)), 'freq': {}, 'prob': {}, 'ent': {}}
    for i in result['info']:
        result['freq'][i] = source.count(i)
        result['prob'][i] = float(result['freq'][i]) / len(source)
        result['ent'][i] = -(result['prob'][i] * math.log(result['prob'][i], 2))
    return result


# ::: Pikslite erinevuse arvutamine :::
def getpixeldiff(source):
    difference = []
    for i in range(len(source)):
        if i == 0:
            difference.append(source[i])
        else:
            difference.append(source[i] - source[i - 1])
    return difference

print('Pikslite arv: %s' % (len(src)))
diff = getpixeldiff(src)
res = getresult(diff)
print('Entroopia: ' + str(sum(res['ent'].values())))

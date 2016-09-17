__author__ = "Arno Kender (163256IATM)"
__version__ = "2.0"
__email__ = "arno.kender@gmail.com"

# ::: Shannoni entroopia arvutamine ASCII tekstifailist :::
import os.path
import math

# ::: Faili lugemine :::
filename = 'input_1.txt'
file = open(filename, 'r')
src = list(file.read())
file.close()


# ::: ASCII kontroll :::
def asciicheck(information):
    passed = []
    for i in information:
        if ord(i) < 128:
            # exit('\nSisend ei vasta ASCII kodeeringule!')
            passed.append(i)
    return passed


# ::: Info sageduse, t6en2osuse ja entroopia arvutamine :::
def getresult(source):
    result = {'info': list(set(source)), 'freq': {}, 'prob': {}, 'ent': {}}
    for i in result['info']:
        result['freq'][i] = source.count(i)
        result['prob'][i] = float(result['freq'][i]) / len(source)
        result['ent'][i] = -(result['prob'][i] * math.log(result['prob'][i], 2))
    return result

print('Symbolite arv algselt: %s' % (len(src)))
src = asciicheck(src)
print('ASCII symbolite arv: %s' % (len(src)))
res = getresult(src)
print('Entroopia: ' + str(sum(res['ent'].values())))

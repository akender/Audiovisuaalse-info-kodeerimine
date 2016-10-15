__author__ = "Arno Kender (163256IATM)"
__version__ = "2.0"
__email__ = "arno.kender@gmail.com"

# ::: Huffmani kooder :::
import json
from math import log


# ::: Custom object :::
class HuffmanNode:
    def __init__(self, probability, symbol=None, left=None, right=None):
        self.probability = probability
        self.symbol = symbol
        self.left = left
        self.right = right

    def isleaf(self) -> bool:
        if self.symbol is not None:
            return True
        else:
            return False


# ::: ASCII kontroll :::
def asciifilter(information) -> list:
    passed = []
    for i in information:
        if ord(i) < 128:
            # exit('\nSisend ei vasta ASCII kodeeringule!')
            passed.append(i)
    return passed


# ::: Info sageduse, t6en2osuse ja entroopia arvutamine :::
def getparams(source) -> dict:
    result = {'information': list(set(source)), 'frequency': {}, 'probability': {}, 'entropy': {}}
    for i in result['information']:
        result['frequency'][i] = source.count(i)
        result['probability'][i] = float(result['frequency'][i]) / len(source)
        result['entropy'][i] = -(result['probability'][i] * log(result['probability'][i], 2))
    return result


# ::: Koodi keskmise pikkuse arvutamine :::
def getavgcodelength(probdict, codedict) -> float:
    result = 0
    for i in probdict:
        result += float(probdict[i]) * float(len(codedict[i]))
    return float(result)


# ::: Koodi liiasuse arvutamine :::
def getredundancy(avgcodelength, entropy) -> float:
    return float(avgcodelength - entropy)


# ::: Koodi efektiivsuse arvutamine :::
def getcompressionratio(uncompressedsource, compressedsource) -> float:
    ucl = ''
    for i in list(uncompressedsource):
        ucl += bin(ord(i))[2:]
    return float(len(ucl) / len(str(compressedsource)))


# ::: Lisa sorteeritud j2rjekorda :::
def nodeinsert(dlist, node):
    for i in range(len(dlist)):
        if float(node.probability) < float(dlist[i].probability):
            dlist.insert(i, node)
            return
    dlist.append(node)
    return


# ::: Tee s6lmede list :::
def makenodelist(paramsdict) -> list:
    result = []
    for i in paramsdict['information']:
        nodeinsert(result, HuffmanNode(paramsdict['probability'][i], i))
    return result


# ::: Tee puu :::
def maketree(nlist) -> HuffmanNode:
    n = nlist
    while len(n) > 1:
        new = HuffmanNode((n[0].probability + n[1].probability), None, n[0], n[1])
        n.remove(n[0])
        n.remove(n[0])
        nodeinsert(n, new)
    return n[0]


#  ::: Tee s6nastikust JSON fail :::
def makejsonfile(data, jsonfilename):
    with open(jsonfilename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile)


# ::: Tagasta kooditabel ja kirjuta faili :::
def getcodetable(node, code='', codetable={}) -> dict:
    if node.isleaf():
        codetable[node.symbol] = code
    else:
        getcodetable(node.left, code + '0', codetable)
        getcodetable(node.right, code + '1', codetable)
    makejsonfile(codetable, 'table_code.json')
    return codetable


# ::: Kodeeri :::
def encode(source, codetable, dstfilename='data_encoded.txt'):
    f = open(dstfilename, 'w')
    result = ''
    for i in list(source):
        f.write(codetable[i])
        result += codetable[i]
    f.close()
    return result


# ::: Dekodeeri :::
def decode(source, rootnode, dstfilename='data_decoded.txt'):
    fd = open(dstfilename, 'w+')
    r = rootnode
    result = ''
    for i in list(source):
        if r.isleaf():
            fd.write(r.symbol)
            result += r.symbol
            r = rootnode
        if i == '0':
            r = r.left
        elif i == '1':
            r = r.right
    fd.close()
    return result


# ::: Faili lugemine :::
sfname = 'input.txt'
# sfname = 'input_test.txt'
# sfname = 'input_test2.txt'
sfile = open(sfname, 'r')
srcl = list(sfile.read())
sfile.close()

print('Symbolite koguarv algselt: %s' % len(srcl))
srcl = asciifilter(srcl)
print('ASCII symbolite koguarv: %s' % len(srcl))
params = getparams(srcl)
print('Tekstis esinenud symbolid (%s): %s' % (len(params['information']), params['information']))
nl = makenodelist(params)
print('Puu lehtede arv: %s' % len(nl))
root = maketree(nl)
ctbl = getcodetable(root)
enc = encode(srcl, ctbl)
dec = decode(enc, root)
ents = sum(params['entropy'].values())
print('\nAllika entroopia: %s bit/sym' % ents)
avg = getavgcodelength(params['probability'], ctbl)
print('Koodi keskmine pikkus: %s bit/sym' % avg)
red = getredundancy(avg, ents)
print('Koodi liiasus: %s bit/sym' % red)
print('\nTihendamise efektiivsus: %s' % getcompressionratio(dec, enc))

__author__ = "Arno Kender (163256IATM)"
__version__ = "4.0"
__email__ = "arno.kender@gmail.com"

# ::: LZW kooder ja dekooder :::


# ::: ASCII kontroll :::
def asciifilter(information) -> list:
    passed = []
    for i in information:
        if ord(i) < 128:
            # exit('\nSisend ei vasta ASCII kodeeringule!')
            passed.append(i)
    return passed


def appendtolimitedlist(item, li=[], limit=1024):
    if len(li) < limit:
        li.append(item)


def getasciitbl() -> list:
    tbl = []
    for i in range(128):
        appendtolimitedlist(chr(i), tbl)
    return tbl


def lzwencode(codetable=[], text='') -> list:
    ctbl = list(codetable)
    code = []
    last = ''
    for i in range(len(list(text))):
        current = text[i]
        combi = last + current
        if combi in ctbl:
            last += current
        else:
            appendtolimitedlist(combi, ctbl)
            index = ctbl.index(last)
            code.append(index + 1)
            last = current
    index = ctbl.index(last)
    code.append(index + 1)
    print('Lõplik tähestik (%s): %s' % (len(ctbl), ctbl))
    return code


def lzwdecode(codetable=[], code=[]) -> str:
    ctbl = list(codetable)
    text = ''
    last_str = ''
    for i in range(len(code)):
        current_code = code[i]
        if current_code <= len(ctbl):
            current_str = ctbl[current_code - 1]
        else:
            current_str = last_str + last_str[0]
        text += current_str
        combi = last_str + current_str[0]
        if combi not in ctbl:
            appendtolimitedlist(combi, ctbl)
        last_str = current_str
    print('Lõplik tähestik (%s): %s' % (len(ctbl), ctbl))
    return text


# srcfile = open('input_test.txt', 'r')
srcfile = open('input.txt', 'r')
srctxt = srcfile.read()
srcfile.close()
srctxt = asciifilter(srctxt)

# src = ['wabbawabba', ['a', 'b', 'w']]
# src = ['wabba_wabba_wabba_wabba_woo_woo_woo', ['_', 'a', 'b', 'o', 'w']]
# src = ['ratatatat_a_rat_at_a_rat', ['a', '_', 'r', 't']]
src = [srctxt, getasciitbl()]
# print('Allikas (%s): %s' % (len(src[0]), src[0]))
print('Algne tähestik (%s): %s' % (len(src[1]), src[1]))
cod = lzwencode(src[1], src[0])
print('Kood (%s): %s' % (len(cod), cod))
print()
print('Kood (%s): %s' % (len(cod), cod))
print('Algne tähestik (%s): %s' % (len(src[1]), src[1]))
decod = lzwdecode(src[1], cod)
# print('Tekst (%s): %s' % (len(decod), decod))

dstfile = open('output.txt', 'w')
dstfile.write(decod)
dstfile.close()

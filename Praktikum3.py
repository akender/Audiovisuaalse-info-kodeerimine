__author__ = "Arno Kender (163256IATM)"
__version__ = "2.0"
__email__ = "arno.kender@gmail.com"

# ::: LZW kooder ja dekooder :::


def getasciitbl():
    tbl = []
    for i in range(128):
        tbl.append(chr(i))
    return tbl


def appendtolimitedlist(item, li=[], limit=1024):
    if len(li) < limit:
        li.append(item)


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
    # print(ctbl)
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
    # print(ctbl)
    return text


srcfile = open('input.txt', 'r')
srctxt = srcfile.read()
srcfile.close()

# src = ['wabbawabba', ['a', 'b', 'w']]
# src = ['wabba_wabba_wabba_wabba_woo_woo_woo', ['_', 'a', 'b', 'o', 'w']]
# src = ['ratatatat_a_rat_at_a_rat', ['a', '_', 'r', 't']]
src = [srctxt, getasciitbl()]
# print(src[0])
print(src[1])
cod = lzwencode(src[1], src[0])
print(cod)
print()
print(cod)
print(src[1])
decod = lzwdecode(src[1], cod)
# print(decod)

dstfile = open('output.txt', 'w')
dstfile.write(decod)
dstfile.close()

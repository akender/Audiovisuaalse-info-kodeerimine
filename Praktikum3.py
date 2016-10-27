__author__ = "Arno Kender (163256IATM)"
__version__ = "2.0"
__email__ = "arno.kender@gmail.com"

# ::: LZW kooder ja dekooder :::


def initiateasciitbl():
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
    print(ctbl)
    return code


def lzwdecode(codetable=[], code=[]) -> str:
    ctbl = list(codetable)
    text = ''
    last_str = ''
    for i in range(len(code)):
        current_code = code[i]
        # p = 'current_code: ' + str(current_code) + ' len(ctbl):' + str(len(ctbl)) + ' last_str:' + last_str
        if current_code <= len(ctbl):
            current_str = ctbl[current_code - 1]
            # p += ' current_str:' + current_str
        else:
            # p += ' [olukord]'
            current_str = last_str + last_str[0]
        text += current_str
        combi = last_str + current_str[0]
        # p += ' combi:' + combi
        if combi not in ctbl:
            appendtolimitedlist(combi, ctbl)
        last_str = current_str
        # p += ' len(ctbl):' + str(len(ctbl)) + ' text:' + text
        # print(p)
        # print(ctbl)
    print(ctbl)
    return text


# src = ['wabbawabba', ['a', 'b', 'w']]
# src = ['wabba_wabba_wabba_wabba_woo_woo_woo', ['_', 'a', 'b', 'o', 'w']]
# src = ['ratatatat_a_rat_at_a_rat', ['a', '_', 'r', 't']]
src = ['ratatatat_a_rat_at_a_rat', initiateasciitbl()]
print(src[0])
print(src[1])
cod = lzwencode(src[1], src[0])
print(cod)
print()
print(cod)
print(src[1])
decod = lzwdecode(src[1], cod)
print(decod)
# print(src[0])

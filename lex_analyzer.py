final = []


def main():
    global final
    testfile = open("fileToParse.java", "r")
    lines = testfile.read().splitlines()
    testfile.close()
    stuff = [' ', ',', '"', '(', ')', '{', '}', ';', '!', '[', ']', '<=', '==',
             '>=', '++', '--', '-=', '+=', '=', '+', '-', '>', '<']

    def lex_line(s):
        arr = []
        start = 0
        for x, z in enumerate(s):
            if(s[x] == '/' and s[x+1] == '/'):
                arr.append(s[start:])
                break
            if(s[x:x+2] in stuff):
                arr.append(s[start:x])
                arr.append(s[x:x+2])
                start = x+2
                continue
            if(s[x] in stuff):
                if(s[x-1:x+1] in stuff):
                    pass
                else:
                    arr.append(s[start:x])
                    arr.append(s[x])
                    start = x+1
                    continue
            if(x == len(s)-1):
                arr.append(s[start:])
        while('' in arr):
            arr.remove('')
        return arr

    for line in lines:
        final.append(lex_line(line))
        for index1, y in enumerate(final):
            for index2, z in enumerate(y):
                while(z.find('\t') != -1):
                    if(z.find('\t') == 0):
                        z = z[z.find('\t')+1:]
                        final[index1][index2] = z[z.find('\t')+1:]
                    else:
                        z = z[0:z.find('\t')+2:]
                        final[index1][index2] = z[0:z.find('\t')+2:]
            while('' in y):
                y.remove('')

# for x in final:
#     print(x)
#


def get_array():
    return final

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
            if(s[x] == '/' and s[x+1] == '/'): #Keeps comments from breaking the code lines
                arr.append(s[start:])
                break
            if(s[x:x+2] in stuff): #If the substring is in stuff, then it saves it in arr, and moves to the next step
                arr.append(s[start:x])
                arr.append(s[x:x+2])
                start = x+2 #start tracks where in the string being processed you are; as the first character that we want in the next substring
                continue
            if(s[x] in stuff):
                if(s[x-1:x+1] in stuff):
                    pass
                else:
                    arr.append(s[start:x]) #Appends Arr with the entire substring from the last pulled character (or the first character) to x
                    arr.append(s[x]) #Appends x to Arr so that x is not forgotten
                    start = x+1 #New Start is the first character after our last substring, so it is x+1
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


def get_array():
    return final

# Main Code and Comments written by Canadia013 prior to v0.0.2-alpha,
# See commit 0585875b4e6c811e17de605c24834e1fbf42263f

final = []


def main():
    global final
    testfile = open("fileToParse.java", "r")
    lines = testfile.read().splitlines()
    testfile.close()
    # stuff contains a list of the traditional characters used in java.
    # This array is used to determine how to separate the items reguardless
    # of spacing.
    stuff = [' ', ',', '"', '(', ')', '{', '}', ';', '!', '[', ']', '<=', '==',
             '>=', '!=', '++', '--', '-=', '+=', '=', '+', '-', '>', '<', ':']

    def lex_line(s):
        arr = []
        start = 0
        for x, z in enumerate(s):
            if(x < len(s)-1):
                # Keeps comments from breaking the code lines by merging
                # the slashes together.
                if(s[x] == '/' and s[x+1] == '/'):
                    arr.append(s[start:])
                    break
            # If the substring is in stuff, then it saves it in the array named
            # arr, and moves to the next step.
            if(s[x:x+2] in stuff):
                arr.append(s[start:x])
                arr.append(s[x:x+2])
                # Start variable tracks where in the string being processed
                # you are; as the first character that we want in the next
                # substring to append:
                start = x+2
                continue

            if(s[x] in stuff):
                if(s[x-1:x+1] in stuff):
                    pass
                else:
                    # If we reach an item in stuff with other items that did
                    # not fit beforehand, this appends to arr with the entire
                    # substring from the last pulled character
                    # (or the first character) to x, then appends the caught
                    # character:
                    arr.append(s[start:x])
                    arr.append(s[x])
                    # Sets start to the next character after caught one:
                    start = x+1
                    continue
            if(x == len(s)-1):
                # If we have reach the end, it will append the remaining items.
                arr.append(s[start:])
        # Final check through to remove empty entries.
        while('' in arr):
            arr.remove('')
        return arr

    for line in lines:
        # Runs the above method per line to get the full array to be sent
        # to the translator. The results are stored in the array final.
        final.append(lex_line(line))

    # For the final array, there needs to be a check for tabs.
    # This is because of python's use of tabs instead of curly braces.
    # The number of tabs needed will be determined by the translator.
    # Therefore, all tabs (indicated as '\t') must be removed at this
    # phase.
    for index1, y in enumerate(final):
        # Begins by itterating through each word.
        for index2, z in enumerate(y):
            # Then itterates by character, as sometimes '\t' is merged with
            # other words.
            while(z.find('\t') != -1):
                # While loop is needed as some words may contain more than one
                # '\t'. E.x. '\t\tsomeVariableName'
                if(z.find('\t') == 0):
                    # Cuts off the '\t', located at the beginning, from final.
                    z = z[z.find('\t')+1:]
                    final[index1][index2] = z[z.find('\t')+1:]
                else:
                    # Cuts off the '\t', located somewher in the center,
                    # from final.
                    z = z[0:z.find('\t')+2:]
                    final[index1][index2] = z[0:z.find('\t')+2:]
        while('' in y):
            y.remove('')

# For debugging purposes.
# for x in final:
#     print(x)
#


def get_array():
    return final

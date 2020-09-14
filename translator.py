import lex_analyzer
import importlib
transarr = []
# translator file that takes an array from a lexical analyzer (Java)
# and translates it to its Python equivalent


def main():
    global transarr
    arr = []
    lex_analyzer.main()
    final = lex_analyzer.final

    for x in final:
        for y in x:
            arr.append(y)
        arr.append('\n')

    transarr = []
    # number_indents = 0
    operators = ['=', '==', '!=', '+=', '-=']

    class_count = 0
    class_name = ''
    class_names = []

    for index, x in enumerate(arr):
        if(x == 'class'):
            class_count = -1
            transarr.append(x)
        elif(x == ' '):
            if(index > 1):
                if(transarr[-1] == ' '):
                    pass
                else:
                    transarr.append(x)
        elif(x == 'private'):
            transarr.append('__')
        elif(x == 'protected'):
            transarr.append('_')
        elif(x == 'void'):
            transarr.append('def')
        elif(x == 'int' or x == 'String' or x == 'short' or x == 'long' or
             x == 'float' or x == 'double' or x == 'void' or x == 'new'):
            if(arr[index+2] == '('):
                transarr.append('def')
            elif(arr[index+3] == '('):
                transarr.append('def')
            else:
                # print(arr[index+2])
                pass
        elif(x == '{'):
            transarr.append(':')
            while(transarr[-2] == '\n' or transarr[-2] == ' '):
                transarr.pop(-2)
            class_count += 1
        elif(x == '}'):
            transarr.append('\t')
            if(class_count > 0):
                class_count -= 1
            if(class_count == 0):
                class_name = ''
        elif(x == '['):
            if(arr[index-1] in operators):
                transarr.append(x)
            else:
                pass
        elif(x == ']'):
            if('[' in transarr):
                transarr.append(x)
            else:
                pass
        elif(x == 'public' or x == 'static' or x == 'final' or x == 'System' or
             x == 'out' or x == 'args'):
            pass
        elif(x == ';'):
            pass
        elif(x[0:4] == 'this'):
            transarr.append('self'+x[4:])
        elif(len(class_name) >= 1 and x == class_name and class_name != ' '):
            transarr.append('def')
            transarr.append(' ')
            transarr.append('__init__')
        elif(x == 'main'):
            class_names.append(class_name)
            class_name = ''
            class_count = 0
            transarr.append(x)
        elif(x == '('):
            transarr.append(x)
            if(index >= 4):
                print(class_count)
                print(transarr[-3])
                print(transarr[-4])
                if(transarr[-3] == 'def' and class_count > 0):
                    transarr.append('self')
                elif(transarr[-4] == 'def' and class_count > 0):
                    transarr.append('self')
        elif(x == ')'):
            if(transarr[-1] == ' ' and transarr[-2] == ','):
                del transarr[-1]
                del transarr[-2]
            transarr.append(x)
        else:
            if(len(transarr) >= 2):
                if(transarr[-2] == 'self' and transarr[-1] != ')'):
                    transarr.append(',')
                    transarr.append(' ')
            if(class_count == -1):
                class_name = x
                print(class_name)
                if(len(class_name) >= 1 and class_name != ' '):
                    class_count = 0
            if('//' in x):
                x = '#' + x[2:]
                # print(x)
            transarr.append(x)
    for index, z in enumerate(transarr):
        if(z == 'System.out.print'):
            transarr[index] = 'print'
            try:
                while(transarr.index(
                    ')', transarr.index('print') > transarr.index('+', index))
                ):
                    transarr[transarr.index('+', index)] = ','
            except ValueError:
                pass
            transarr.insert(transarr.index(
                ')', index), ", end = ''")
        if(z == 'System.out.println'):
            transarr[index] = 'print'
        if(z == 'if'):
            try:
                if(transarr[transarr.index(')', index)+1] != ':'):
                    transarr.insert(transarr.index(
                        ')', index)+1, ':')
                    transarr.insert(transarr.index(
                        '\n', transarr.index('\n', index)+1), '\t')
            except ValueError:
                pass
        if(z == '\n' or z == '_' or z == '__' or z == "("):
            if(index != len(transarr)-1):
                while(transarr[index+1] == ' '):
                    del transarr[index+1]
        if(z == 'for'):
            try:
                x = transarr.index('(', index+1)
                y = transarr.index(')', index+1)
                q = transarr.index('=', index+1)
                variable_name = transarr[x+1]
                if(x != 1 and y != -1):
                    if(q < y):
                        print(transarr[x:y+1])
                        bool_local = 0
                        maximum_modifier = ""
                        u = x+1
                        incriment_modifier = ""
                        while(u < y):
                            if(transarr[u] == '>='):
                                bool_local = u
                                u += 1
                                maximum_modifier = " - 1"
                            elif(transarr[u] == '<='):
                                maximum_modifier = " + 1"
                                bool_local = u
                                u += 1
                                print("Here <=")
                            elif(transarr[u] == '>' or transarr[u] == '<'):
                                bool_local = u
                                u += 1
                            elif(transarr[u] == '++'):
                                u += 1
                            elif(transarr[u] == '-='):
                                for o in transarr[u+1:y]:
                                    if(o != variable_name):
                                        incriment_modifier = incriment_modifier + o
                                    else:
                                        while(incriment_modifier.endswith(" ")):
                                            incriment_modifier = incriment_modifier[:-1]
                                while(incriment_modifier.endswith("+") or
                                      incriment_modifier.endswith("-")or
                                      incriment_modifier.endswith(" ")):
                                    incriment_modifier = incriment_modifier[:-1]
                                while(incriment_modifier.startswith("+") or
                                      incriment_modifier.startswith(" ")):
                                    incriment_modifier = incriment_modifier[1:]
                                incriment_modifier = "-(" + incriment_modifier + ")"
                                u += 1
                            elif(transarr[u] == '+='):
                                for o in transarr[u+1:y]:
                                    if(o != variable_name):
                                        incriment_modifier = incriment_modifier + o
                                u += 1
                            elif(transarr[u] == '=' and u > q):
                                for o in transarr[u+2:y]:
                                    if(o != variable_name):
                                        incriment_modifier = incriment_modifier + o
                                    elif(incriment_modifier.endswith("-") or incriment_modifier.endswith("- ")):
                                        tab_count = 1
                                        first_line_local = transarr.index(
                                            '\n', q+1)
                                        while(tab_count != 0):
                                            second_line_local = transarr.index(
                                                '\n', first_line_local+1)
                                            tab_count = tab_count + transarr[first_line_local:second_line_local].count(
                                                ':') - transarr[first_line_local:second_line_local].count(
                                                    '\t')
                                            first_line_local = int(second_line_local)
                                        tab_count = transarr[0:second_line_local].count(
                                            ':')
                                        while(incriment_modifier.endswith("-") or incriment_modifier.endswith(" ")):
                                            incriment_modifier = incriment_modifier[:-1]
                                        transarr.insert(first_line_local-1,
                                                        "".join(variable_name + " = -" + variable_name))
                                    else:
                                        if(incriment_modifier.endswith("+ ")):
                                            incriment_modifier = incriment_modifier[:-3]

                                u += 1
                            elif(transarr[u] == '--'):
                                incriment_modifier = "-1"
                                u += 1
                            elif(transarr[u] == " " or transarr[u] == ''):
                                del transarr[u]
                                if(u < q):
                                    q -= 1
                                if(u < bool_local):
                                    bool_local -= 1
                                y -= 1
                                variable_name = transarr[x+1]
                            elif(transarr[u] == '-=' or transarr[u] == '+='):
                                incriment_modifier = transarr[u+1:y]
                                u += 1
                            else:
                                u += 1
                        while(incriment_modifier.endswith("+") or
                              incriment_modifier.endswith("-")or
                              incriment_modifier.endswith(" ")):
                            incriment_modifier = incriment_modifier[:-1]
                        while(incriment_modifier.startswith("+") or
                              incriment_modifier.startswith(" ")):
                            incriment_modifier = incriment_modifier[1:]
                        if not incriment_modifier == "":
                            text = " {0} in range({1}, {2}, {3})"\
                                "".format(transarr[x+1],
                                          ''.join(transarr[q+1:bool_local-1
                                                           ]),
                                          ''.join(transarr[bool_local+1]
                                                  ) + maximum_modifier,
                                          ''.join(incriment_modifier))
                        else:
                            text = " {0} in range({1}, {2})"\
                                "".format(transarr[x+1],
                                          ''.join(transarr[q+1:bool_local-1]),
                                          ''.join(transarr[bool_local+1]
                                                  ) + maximum_modifier)
                        print(text)
                        del transarr[x:y+1]
                        transarr.insert(x, text)
            except ValueError:
                pass
    for y in class_names:
        transarr.append(y+".main()")
    print(transarr[0:])


importlib.reload(lex_analyzer)

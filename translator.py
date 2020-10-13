import lex_analyzer
import importlib
transarr = []
# translator file that takes an array from a lexical analyzer (Java)
# and translates it to its Python equivalent.


def main():
    global transarr
    arr = []
    lex_analyzer.main()
    final = lex_analyzer.final

    # Converts the given array of arrays (array of lines) into a single array
    # with '\n' indicating a new line.
    for x in final:
        for y in x:
            arr.append(y)
        arr.append('\n')

    # As classes are in both JAVA and python, but not required in python,
    # a list of class names are used in case the JAVA file has a "main" method.
    class_count = 0
    class_name = ''
    class_names = []

    ignore_semicolon = False
    in_quotes = False
    has_array = False
    single_line_elseif = False

    # This array goes through two sets of loops through the array.
    # The first one below goes through the Java terms that can be swiftly
    # be translated to its Python equivalent.
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
                pass
        elif(x == '{'):
            single_line_elseif = False
            if(transarr[-1].startswith('#') or transarr[-1] == ' ' or
               transarr[-1] == '\n'):
                tempindex = -2
                while(transarr[tempindex].startswith('#') or
                      transarr[tempindex] == ' ' or
                      transarr[tempindex] == '\n'):
                    tempindex -= 1
                transarr.insert(tempindex+1, ':')
            else:
                print(transarr[-1])
                transarr.append(':')
            while(transarr[-2] == '\n' or transarr[-2] == ' '):
                transarr.pop(-2)
            class_count += 1
        elif(x == '}'):
            transarr.append('\t')
            if(single_line_elseif):
                tempindex = search(['else', 'if'], transarr, -1, -1)
                tempindex = search(['\n'], transarr, tempindex, 1)
                tempindex = search([' ', ')', 'else', 'if'],
                                   transarr, tempindex, -1)
                transarr.insert(tempindex+1, ':')
                single_line_elseif = False
            if(class_count > 0):
                class_count -= 1
            if(class_count == 0):
                class_name = ''
        elif(x == '['):
            if(transarr[-1] == ' ' and (transarr[-2] == '\n' or
                                        transarr[-2] == '\t')):
                del transarr[-1]
                pass
            elif(transarr[-1] == '\n' or transarr[-1] == '\t' or
                 transarr[-1] == '('):
                pass
            else:
                has_array = True
                transarr.append(x)
        elif(x == ']'):
            if(has_array):
                transarr.append(x)
            else:
                pass
        elif(x == 'public' or x == 'static' or x == 'final' or x == 'System' or
             x == 'out' or x == 'args'):
            pass
        elif(x == ';'):
            # TODO
            tempindex = search([' '], arr, index+1, 1)
            if tempindex is not None:
                if(arr[tempindex] != '\n' and not ignore_semicolon):
                    transarr.append('\n')
                else:
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
                if(transarr[-3] == 'def' and class_count > 0):
                    transarr.append('self')
                elif(transarr[-4] == 'def' and class_count > 0):
                    transarr.append('self')
        elif(x == ')'):
            if(transarr[-1] == ' ' and transarr[-2] == ','):
                del transarr[-1]
                del transarr[-2]
            transarr.append(x)
        elif(x == 'for' or x == 'while'):
            ignore_semicolon = True
            transarr.append(x)
        elif(x == '\n'):
            ignore_semicolon = False
            has_array = False
            transarr.append(x)
        elif(x == 'else' or x == 'if'):
            single_line_elseif = True
            transarr.append(x)
        else:
            if(len(transarr) >= 2):
                if(transarr[-2] == 'self' and transarr[-1] != ')'):
                    transarr.append(',')
                    transarr.append(' ')
            if(class_count == -1):
                class_name = x
                if(len(class_name) >= 1 and class_name != ' '):
                    class_count = 0
            if('//' in x):
                x = '# ' + x[2:]
            transarr.append(x)

    # This second array goes through the more complicated methods used in JAVA
    # and factors in changing parameters.
    # The following methods are accounted for here:
    # for loops, if statements, 'System.out.print', and 'System.out.println'
    for index, z in enumerate(transarr):
        if(z == '\"' or z == '\''):
            if(transarr[index-1] == "\\"):
                pass
            else:
                in_quotes = not in_quotes
                continue
        elif(in_quotes):
            continue
        if(z == '++'):
            incriment = reverse_search([' ', ''], transarr, index-1, -1)
            del transarr[incriment+1:index+1]
            transarr.insert(index, " = {0} + 1"
                            .format(transarr[incriment]))
        elif(z == '--'):
            incriment = reverse_search([' ', ''], transarr, index-1, -1)
            del transarr[incriment+1:index+1]
            transarr.insert(index, " = {0} - 1"
                            .format(transarr[incriment]))
        # The two System.out's need to be checked here as to not conlfict with
        # the first loop through
        elif(z == 'System.out.print'):
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
        elif(z == 'System.out.println'):
            transarr[index] = 'print'
        elif(z == 'if'):
            try:
                if(transarr[transarr.index(')', index)+1] != ':'):
                    transarr.insert(transarr.index(
                        ')', index)+1, ':')
                    transarr.insert(transarr.index(
                        '\n', transarr.index('\n', index)+1), '\t')
            except ValueError:
                pass
        elif(z == '\n' or z == '_' or z == '__' or z == "("):
            if(index != len(transarr)-1):
                while(transarr[index+1] == ' '):
                    del transarr[index+1]

        # When it comes to for loops, there are multiple formats that JAVA
        # allows. With such, several checks must be made to determine how it
        # is configured. The comments for this section will show examples
        # that they are catching for.
        # NOTE: for loops are merged into a single string after translation
        # NOTE: in the array.
        # TODO: Need to add support for JAVA for(Item:Array) loops
        elif(z == 'for'):
            # The try/excepts are due to the index method throwing a ValueError
            # if it cannot find the core aspects of a for loop. Pretty handy
            # huh? :D
            try:
                # Inserting a new line for adding a declaration statement for
                # the assignment. The assignment is placed before the actual
                # for loop to maximize flexibility of input code. If it is
                # redundant, it must be removed by hand after translation.
                # Blame python's for loop implementation for the redundancy,
                # not me. :)
                transarr.insert(index, '\n')
                # Main components of a for loop:
                # x is the opening parenthesis' index
                # y is the closing parenthesis' index
                # q is the first statement's assignment's index.
                x = transarr.index('(', index+1)
                y = transarr.index(')', index+1)
                q = transarr.index('=', index+1)

                # variable_name is for use involving using the variable name
                # in the iteration statement. This will be the first
                # non-whitespace string from the array.
                variable_name = transarr[x+1]
                # tempindex serves two purposes: This first use is to help
                # determine what the variable name in use for the loop is
                # located, reguardless of whitespace.
                tempindex = reverse_search(['', ' '], transarr, x+1, 1)
                variable_name = transarr[tempindex]
                # while(variable_name == '' or variable_name == ' '):
                #     tempindex = tempindex+1
                #     variable_name = transarr[x+tempindex]

                # As some statements have varying sizes, I have the following:
                # bool_local_start and bool_local_end are the begginning and
                # end of the boolean condition to be checked at the end of
                # every for loop iteration.
                bool_local_start = 0
                bool_local_end = 0
                # maximum_modifier will contain any extra parameters to be
                # added to the boolean condition (such as <= would yield a
                # +1 to match the proper conditions).
                maximum_modifier = ""
                # tempindex's second purpose is to signify the start of where
                # we are scanning for information in the upcomming 'while' loop
                tempindex = x+1
                # incriment_modifier stores how we are to incriment in the
                # loop.
                incriment_modifier = ""
                # incriment_positive is for the special conditions
                # '++' and '--'
                incriment_special = False
                # To maximize flexibility, some for loops will be translated
                # into while loops.
                change_to_while = False

                # This is a while loop instead of a for loop is due to the
                # possibility of white space or blank statements.
                # these need to be removed for the loop to be NEATLY
                # translated. With such, it is removed from transarr
                # and not incrimented.
                # This while loop sets the final needed parameters to the for
                # loop, such as the maximum/minimum modifier (for <= and >=),
                # the location of the boolean information's start and end
                # (bool_local_start and bool_local_end), and the
                # amount you are incrimenting by (incriment_modifier).
                while(tempindex < y):
                    if(transarr[tempindex] == '>='):
                        bool_local_start = tempindex
                        tempindex += 1
                        maximum_modifier = " - 1"
                    elif(transarr[tempindex] == '<='):
                        maximum_modifier = " + 1"
                        bool_local_start = tempindex
                        tempindex += 1
                    elif(transarr[tempindex] == '=='):
                        change_to_while = True
                        bool_local_start = tempindex
                        tempindex += 1
                    elif(transarr[tempindex] == '>'
                         or transarr[tempindex] == '<'
                         or transarr[tempindex] == '!='):
                        bool_local_start = tempindex
                        tempindex += 1
                    elif(transarr[tempindex] == '++'):
                        incriment_special = True
                        bool_local_end = tempindex-1
                        tempindex += 1
                    elif(transarr[tempindex] == '-='):
                        for o in transarr[tempindex+1:y]:
                            if(o != variable_name):
                                incriment_modifier = incriment_modifier + o
                            else:
                                while(incriment_modifier.endswith(" ")):
                                    incriment_modifier = incriment_modifier[
                                        :-1]
                        # Remove trailing whitespace before enveloping
                        # the text inside '-()'
                        remove_whitespace_edges(incriment_modifier)
                        incriment_modifier = "- (" + incriment_modifier + ")"
                        bool_local_end = tempindex-1
                        tempindex += 1
                    elif(transarr[tempindex] == '+='):
                        for o in transarr[tempindex+1:y]:
                            incriment_modifier = incriment_modifier + o + " "
                        bool_local_end = tempindex-1
                        tempindex += 1
                    elif(transarr[tempindex] == '=' and tempindex > q):
                        change_to_while = True
                        for o in transarr[tempindex+1:y]:
                            if(o == ' ' or o == ''):
                                pass
                            else:
                                incriment_modifier = incriment_modifier + o\
                                    + " "
                        bool_local_end = tempindex-1
                        tempindex += 1
                    elif(transarr[tempindex] == '--'):
                        incriment_special = True
                        incriment_modifier = "- 1"
                        bool_local_end = tempindex-1
                        tempindex += 1
                    elif(transarr[tempindex] == " "
                         or transarr[tempindex] == ''):
                        del transarr[tempindex]
                        if(tempindex < q):
                            q -= 1
                        if(tempindex < bool_local_start):
                            bool_local_start -= 1
                        y -= 1
                    else:
                        tempindex += 1
                transarr.insert(index-1, variable_name + " = " +
                                "".join(transarr[q+1:bool_local_start-1]))
                transarr.insert(index-1, "\n")
                q = q+2
                bool_local_start = bool_local_start + 2
                bool_local_end = bool_local_end + 2

                # Extra whitespace cleanup, if any. May be redundant
                remove_whitespace_edges(incriment_modifier)
                #
                # Where the final merge happens.
                # NOTE:If the boolean condition is either == or !=, then the
                # NOTE:for loop becomes a while loop. I take this and rearrange
                # NOTE:the already gathered data and put them in their proper
                # NOTE:spots so that the while loop works correctly.
                # NOTE: This also applies to conditions when the incriment
                # NOTE: statement is '='. This is to maximize flexibility
                # NOTE: of input code. Again, python not me. :^)
                #
                if(transarr[bool_local_start] != '=='
                   and transarr[bool_local_start] != '!=' and
                   not change_to_while):
                    if(incriment_modifier != ""):
                        text = "for {0} in range({1}, {2}, {3})"\
                            "".format(variable_name,
                                      ''.join(transarr[q+1:bool_local_start-1
                                                       ]),
                                      ' '.join(transarr[bool_local_start+1:
                                                        bool_local_end]
                                               ) + maximum_modifier,
                                      ''.join(incriment_modifier))
                    else:
                        text = "for {0} in range({1}, {2})"\
                            "".format(variable_name,
                                      ''.join(transarr[q+1:
                                                       bool_local_start-1]),
                                      ' '.join(transarr[bool_local_start+1:
                                                        bool_local_end]
                                               ) + maximum_modifier)
                    del transarr[index+2:y+3]
                else:
                    text = "while({0} {1} {2})"\
                        "".format(variable_name, transarr[bool_local_start],
                                  ' '.join(transarr[bool_local_start+1:
                                                    bool_local_end]))
                    if(incriment_special):
                        transarr.insert(get_end_of_block(y+1),
                                        ''.join(variable_name + "="
                                                + variable_name + " "
                                                + incriment_modifier))
                    else:
                        if(transarr[bool_local_end+1] == "+="):
                            transarr.insert(get_end_of_block(y+1),
                                            ''.join(variable_name + " = "
                                                    + variable_name + " + "
                                                    + incriment_modifier))
                        elif(transarr[bool_local_end+1] == "-="):
                            transarr.insert(get_end_of_block(y+1),
                                            ''.join(variable_name + " = "
                                                    + variable_name + " "
                                                    + incriment_modifier))
                        else:
                            transarr.insert(get_end_of_block(y+1),
                                            ''.join(variable_name + " = "
                                                    + incriment_modifier))
                    while(transarr[x-1] == ' ' or transarr[x-1] == "for"):
                        del transarr[x-1]
                    del transarr[index+2:y+3]
                if(transarr[x-1] == '\n'):
                    transarr.insert(x, text)
                else:
                    transarr.insert(x-1, text)
                if(transarr[x] == "\n"):
                    del transarr[x]
                if(transarr[x] == ":"):
                    transarr.insert(x+1, '\n')
            except ValueError:
                pass
    for y in class_names:
        if(y != ' ' and y != ''):
            transarr.append(y+".main()")
    if(transarr[-1][-7:] != '.main()'):
        if(search(['main'], transarr, 0, 1) is not None):
            transarr.append("main()")

    # Final removal of all whitespace, if any.
    while(transarr[0] == ' '):
        del transarr[0]
    while(transarr[-1] == ' '):
        del transarr[-1]

    print(transarr[0:])


# Performs a series of checks and determines where the end of the code block
# is.
def get_end_of_block(start_position):
    try:
        first_line_local = transarr.index(
            '\n', start_position+1)
        tab_count = 1
        while(tab_count != 0):
            second_line_local = transarr.index(
                '\n', first_line_local+1)
            tab_count = tab_count +\
                transarr[first_line_local:
                         second_line_local].count(
                    ':') - transarr[
                    first_line_local:
                    second_line_local].count('\t')
            first_line_local = int(second_line_local)
        tab_count = transarr[0:second_line_local]\
            .count(':')
        return first_line_local-1
    except ValueError:
        return None


# So long as we know where the new block should begin (say we are working
# with a for loops), this method gets the next line that begins the code block.
def get_start_of_block(start_position):
    return transarr.index("\n", start_position)


# Used specifically for the for and while loops, this removes unneeded code
# segments and white space.
def remove_whitespace_edges(text):
    while(text.endswith("+") or
          text.endswith("-")or
          text.endswith(" ")):
        text = text[:-1]
    while(text.startswith("+") or
          text.startswith(" ")):
        text = text[1:]
    return text


def search(array_of_searches, array, index, direction):
    try:
        while(array[index] not in array_of_searches):
            if(array[index].startswith('#')):
                index += 1*direction
                break
            print(array[index])
            index += 1*direction
        return index
    except IndexError:
        return None


def reverse_search(array_of_searches, array, index, direction):
    while(array[index] in array_of_searches):
        print(array[index])
        index += 1*direction
    return index


importlib.reload(lex_analyzer)

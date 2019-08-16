#!/usr/bin/env python3

def read_from(x):
    file = open(x, 'r')
    contents = file.read()
    file.close()
    return contents

def is_string(x):
    return len(x) > 1 and x[0] == '\"' and x[-1] == '\"'

def is_number(x):
    try:
        _ = float(x)
    except:
        return False
    return True

def tokenize(x):
    """takes a JSON-ecoded string and returns a list of tokens"""
    
    tokens = []
    i = 0
    while i < len(x):
        # tokenize special characters
        if x[i] == '{':
            tokens.append('{')
            i += 1
        elif x[i] == '}':
            tokens.append('}')
            i += 1
        elif x[i] == '[':
            tokens.append('[')
            i += 1
        elif x[i] == ']':
            tokens.append(']')
            i += 1
        elif x[i] == ',':
            tokens.append(',')
            i += 1
        elif x[i] == ':':
            tokens.append(':')
            i += 1

        # tokenize strings
        elif x[i] == '\"':
            buf = '\"'
            i += 1
            while x[i] != '\"':
                buf += x[i]
                i += 1
            buf += x[i]
            i += 1
            tokens.append(buf)

        # tokenize numbers
        elif x[i] in '-1234567890.':
            buf = x[i]
            i += 1
            decimal = (buf == '.')
            while x[i] in '1234567890' or (not decimal and x[i] == '.'):
                buf += x[i]
                decimal = (x[i] == '.')
                i += 1
            if buf == '.' or buf == '-.' or buf == '-':
                # invalid number
                return None
            else:
                tokens.append(buf)

        # tokenize key words
        elif x[i:i+4] == 'true':
            tokens.append('true')
            i += 4
        elif x[i:i+5] == 'false':
            tokens.append('false')
            i += 5
        elif x[i:i+4] == 'null':
            tokens.append('null')
            i += 4

        # skip all whitespace
        elif x[i] in ' \n\t':
            i += 1

        # invalid
        else:
            return None

    return tokens

def parse(x):
    """parses a list of JSON tokens into a dictionary of dictionaries"""

    # check for opening curly brace
    if x[0] != '{':
        print('no opening brace; returning None...')
        return None

    # check for closing curly brace
    if x[-1] != '}':
        print('no closing curly brace; returning None...')
        return None

    # initialize object
    obj = {}

    i = 1  # already checked opening curly brace
    while True:
        # get key
        if not is_string(x[i]):
            #print('key was not string; returning None...')
            return None
        key = x[i][1:-1]  # slicing removes outer quotes
        i += 1

        # get colon
        if x[i] != ':':
            print('no colon; returning None...')
            return None
        i += 1

        # get (non-key) string
        if is_string(x[i]):
            obj[key] = x[i][1:-1]  # slicing removes quotes
            i += 1

        # get numerical
        if is_number(x[i]):
            obj[key] = x[i][1:-1]  # slicing removes quotes
            i += 1

        # get keywords
        elif x[i] == 'null':
            obj[key] = None
            i += 1

        elif x[i] == 'true':
            obj[key] = True
            i += 1

        elif x[i] == 'false':
            obj[key] = False
            i += 1

        # parse objects recursively
        elif x[i] == '{':
            brace_ct = 1
            j = i
            while brace_ct > 0:
                j += 1
                brace_ct += 1 if x[j] == '{' else 0
                brace_ct -= 1 if x[j] == '}' else 0

            obj[key] = parse(x[i:j+1])
            i = j + 1

        if x[i] != ',':
            break

        i += 1

    return obj

def decode(x):
    """Decode a JSON-encoded string into a dictionary of dictionaries"""
    return parse(tokenize(x))

def encode(x):
    """Encode a dictionary of dictionaries into a string with JSON"""
    json = '{'
    first = True
    for key in x:
        # check all keys are of type string
        if type(key) != str:
            return None

        # add a comma before every key-value pair except the first
        if not first:
            json += ', '
        first = False

        # grab value
        val = x[key]

        # handle values with type string
        if type(val) == str:
            json += key + ': "' + val + '"'

        # handle values with type number
        elif type(val) == int or type(val) == float:
            json += key + ': ' + val

        # handle keyword values
        elif val == True:
            json += key + ': true'

        elif val == False:
            json += key + ': false'

        elif val == None:
            json += key + ': null'

        # handle recursive object case
        elif type(val) == dict:
            json += key + ': ' + encode(val)
            #json += '{}'

    json += '}'

    return json


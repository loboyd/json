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
                raise ValueError('shitty JSON: specific definition of number is evidently unclear')
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
            raise ValueError('shitty JSON: found unexpected token: {}'.format(x[i]))

    return tokens

def parse(x, ind=0):
    """ Parse a list of JSON tokens into a dictionary of dictionaries

    The `i` parameter is for calling the function recursively with a different
    starting index (the starting index of the nested JSON object).
    """

    # check for opening curly brace
    if x[0] != '{':
        raise ValueError('shitty JSON: expected opening curly brace')

    # check for closing curly brace
    if x[-1] != '}':
        raise ValueError('shitty JSON: expected closing curly brace')

    # initialize object
    obj = {}

    i = ind + 1  # already checked opening brace
    while x[i] != '}':
        # get key
        if not is_string(x[i]):
            raise ValueError('shitty JSON: non-string key found')
        key = x[i][1:-1]  # slicing removes outer quotes
        i += 1

        # get colon
        if x[i] != ':':
            raise ValueError('shittyJSON: expected a colon')
        i += 1

        # get (non-key) string
        if is_string(x[i]):
            obj[key] = x[i][1:-1]  # slicing removes quotes
            i += 1

        # get numerical
        if is_number(x[i]):
            obj[key] = x[i]
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

        # parse objects recursively; update index (this is linear time)
        elif x[i] == '{':
            obj[key], i = parse(x, i)

        if x[i] != ',':
            break

        i += 1

    if ind:
        return obj, i+1
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
            raise ValueError('all keys must be of type `str`')

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


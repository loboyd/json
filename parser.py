#!/usr/bin/env python3

def read_from(x):
    file = open(x, 'r')
    contents = file.read()
    file.close()
    return contents

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
    if x[0] != '{':
        print('no opening brace; returning None...')
        return None
    if x[-1] != '}':
        print('no closing brace; returning None...')
        return None

    # initialize object
    obj = {}

    i = 0
    while True:
        # get key's first quote
        while x[i] != '\"':
            i += 1
        i += 1

        # buffer everything up to key's second quote
        key_buf = ''
        while x[i] != '\"':
            key_buf += x[i]
            i += 1
        i += 1

        # get colon
        if x[i] != ':':
            print('no colon; returning None...')
            return None

        # get opening brace
        while x[i] != '{':
            i += 1
        brace_ct = 1

        # buffer everything up to appropriate closing brace
        value_buf = '{'
        while brace_ct > 0:
            i += 1
            if x[i] == '}':
                brace_ct -= 1
            elif x[i] == '{':
                brace_ct += 1
            # buffer after advance so we get the closing brace
            value_buf += x[i]

        # add to object
        obj[key_buf] = parse(value_buf)

        i += 1
        if x[i] != ',':
            break

    return obj

def decode(x):
    """Decodes a JSON-encoded string into a dictionary of dictionaries"""
    return parse(tokenize(x))

def parse_simple(x):
    """parses a JSON-encoded string into a dictionary of dictionaries"""
    x = x.strip()
    if x == '{}':
        return ''
    if x[0] != '{':
        print('no opening brace; returning None...')
        return None
    if x[-1] != '}':
        print('no closing brace; returning None...')
        return None

    # initialize object
    obj = {}

    i = 0
    while True:
        # get key's first quote
        while x[i] != '\"':
            i += 1
        i += 1

        # buffer everything up to key's second quote
        key_buf = ''
        while x[i] != '\"':
            key_buf += x[i]
            i += 1
        i += 1

        # get colon
        if x[i] != ':':
            print('no colon; returning None...')
            return None

        # get opening brace
        while x[i] != '{':
            i += 1
        brace_ct = 1

        # buffer everything up to appropriate closing brace
        value_buf = '{'
        while brace_ct > 0:
            i += 1
            if x[i] == '}':
                brace_ct -= 1
            elif x[i] == '{':
                brace_ct += 1
            # buffer after advance so we get the closing brace
            value_buf += x[i]

        # add to object
        obj[key_buf] = parse(value_buf)

        i += 1
        if x[i] != ',':
            break

    return obj


if __name__ == '__main__':
    #contents = read_from('simple_example.txt')
    contents = read_from('number_example.txt')
    print('JSON example:')
    print(contents, '\n\n')
    print('tokenized:')
    print(tokenize(contents))
    #for token in tokenize(contents):
        #print(token)





""" scratch-work
{
    "key1": <value1>,
    "key2": <value2>,
    "key3": <value3>
}

tokens:
  - strings
  - numbers
  - `true`
   -`false`
  - `null`
  - `:`
  - `,`
  - `{`
  - `}`
  - `[`
  - `]`

"""


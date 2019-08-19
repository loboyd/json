
def pp(x, depth=0):
    """Print a JSON-like object in a nice way"""
    
    indent = 4  # number of spaces per indentation

    for key in x:
        value = x[key]
        if type(value) == dict:
            print('{}:'.format(key))
            pp(value, depth+1)
        else:
            print('{}{}:{}'.format(' '*indent*depth, key, value))


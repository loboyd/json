#!/usr/bin/env python3

from parser import *

contents = read_from('example_without_array.json')

print('JSON example:')
print(contents)

print('\n\ndecoded:')
print(decode(contents))


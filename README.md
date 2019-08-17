This repo implements a simple JSON decoder. Right now, I believe it can decode
any JSON not containing arrays. It contains a separate lexer and parser, and
decodes into a dictionary of dictionaries.

Right now, there is a strange bug with parsing numbers. Run `./main.py` and look
in the `age` field to see it.

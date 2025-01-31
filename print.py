from sys import stderr

_print = print

def print(*args, sep='', **kwargs):
    _print(*args, sep=sep, **kwargs)

def printerr(*args, **kwargs):
    print(*args, **kwargs, file=stderr)


import functools


def compose_two_functions(f, g):
    return lambda *a, **kw: f(g(*a, **kw))


def compose(*funcs):
    return functools.reduce(compose_two_functions, funcs)


def flow(*funcs):
    return functools.reduce(compose_two_functions, funcs[::-1])

# coding: utf-8

import numbers

class Matcher(object):
    def match(target, params):
        return False


class Var(Matcher):
    def __init__(self, name):
        self.name = name
        self.value = None

    def match(self, target, params):
        if self.name in params:
            return params[self.name] == target
        params[self.name] = target
        return True


class Any(Matcher):
    '''
    >>> Any([1,3,5]).match(1, {})
    True
    >>> Any([1,3,5]).match(4, {})
    False
    >>> Any('abc').match('c', {})
    True
    >>> Any('abc').match('x', {})
    False
    >>> Any().match('everything', {})
    True
    >>> params = {}
    >>> Any([(1, Var('a')), (2, Var('b'))]).match((1, 100), params)
    True
    >>> params
    {'a': 100}
    '''
    def __init__(self, elems=None):
        if not elems:
            self.elems = []
        else:
            self.elems = elems

    def match(self, target, params):
        if not self.elems:
            return True

        for e in self.elems:
            if match(target, e, params):
                return True
        return False


def switch(target, *args):
    '''
    switch(target, pattern1, value1, pattern2, value2, ...[, default_value])

    Match target against each patterns (1, 2, ...) and
    return value<n> if the pattern<n> matches.

    Simple cases:

    >>> from pattern import switch
    >>> switch('B',
    ...        'A', 1,
    ...        'B', 2,
    ...        'C', 3)
    2
    >>>

    >>> switch([1, 'x', 1.23],
    ...        [1, 'x', 1.23], 'A',
    ...        [2, 'y', 4.56], 'B',
    ...        [3, 'z', 7.89], 'C')
    'A'
    >>>

    When no match was found, default_value or None will be returned.

    >>> switch('X',
    ...        'A', 1,
    ...        'B', 2,
    ...        'C', 3)
    >>>
    >>> switch('X',
    ...        'A', 1,
    ...        'B', 2,
    ...        'C', 3,
    ...        -1)
    -1
    >>>

    Any() object match any elements in it.

    >>> from pattern import Any
    >>> switch(65,
    ...        Any(range(1, 60)), 'F',
    ...        Any(range(61, 80)), 'C',
    ...        Any(range(81, 90)), 'B',
    ...        Any(range(91, 100)), 'A')
    'C'
    >>>
    >>> switch('e',
    ...        Any('aeiou'), True,
    ...        False)
    True
    >>>

    If value<n> is callable, it is call()ed and returns its return value.

    >>> def f1():
    ...   print 'f1:'
    >>> def f2(a='', b=''):
    ...   print 'f2: a=%s, b=%s'%(a,b)
    >>> def f3(i1=0, i2=0):
    ...   print 'f3: i1=%d, i2=%d'%(i1, i2)
    ...   return i1*i2
    >>> switch(('A', 'B', 'C'),
    ...        ('A', 'B', 'C'), f1,
    ...        ('D', 'E', 'F'), f2,
    ...        ('G', 'H', 'I'), f3)
    f1:

    Var(<name>) in a pattern is variable specifier.  It will match
    anything in the target and its value will be passed to corresponding
    (callable) value as a named parameter.

    >>> from pattern import Var
    >>> switch(('X', 'Y', 'Z'),
    ...        ('A', 'B', 'C'), f1,
    ...        ('X', Var('a'), Var('b')), f2,
    ...        ('I', Var('i1'), Var('i2')), f3)
    f2: a=Y, b=Z
    >>> switch(('I', 6, 7),
    ...        ('A', 'B', 'C'), f1,
    ...        ('X', Var('a'), Var('b')), f2,
    ...        ('I', Var('i1'), Var('i2')), f3)
    f3: i1=6, i2=7
    42

    Var()s of same name matches the same values.

    >>> switch(('I', 6, 7),
    ...        ('A', 'B', 'C'), f1,
    ...        ('X', Var('a'), Var('b')), f2,
    ...        ('I', Var('i1'), Var('i1')), f3)
    >>> switch(('I', 5, 5),
    ...        ('A', 'B', 'C'), f1,
    ...        ('X', Var('a'), Var('b')), f2,
    ...        ('I', Var('i1'), Var('i1')), f3)
    f3: i1=5, i2=0
    0

    Other trivial examples:

    >>> switch(('None', None, None),
    ...        ('A', 'B', 'C'), f1,
    ...        ('X', Var('a'), Var('b')), f2,
    ...        ('I', Var('i1'), Var('i2')), f3)
    >>>
    >>> switch(('A', 'B'),
    ...        ('A', 'B', 'C'), f1,
    ...        ('X', Var('a'), Var('b')), f2,
    ...        ('I', Var('i1'), Var('i2')), f3)
    >>>
    '''
    patterns = [(args[i], args[i + 1]) for i in range(0, len(args) - 1, 2)]
    default_value = extract_default_value(args)

    for pattern, value in patterns:
        params = {}
        if match(target, pattern, params):
            return eval_value(value, params)
    return eval_value(default_value, {})


def eval_value(value, params):
    if callable(value):
        return value(**params)
    else:
        return value


def extract_default_value(args):
    if len(args) % 2 == 1:
        return args[-1]
    else:
        return None


def match(target, pattern, params):
    if is_matcher(pattern):
        return pattern.match(target, params)
    else:
        if type(target) != type(pattern):
            return False
        if is_atom(pattern):
            return True if target == pattern else False
        elif is_sequence(pattern):
            if match_sequence(target, pattern, params):
                return True
    return False


def is_matcher(v):
    return isinstance(v, Matcher)


def is_atom(v):
    return isinstance(v, (str, unicode, numbers.Number))


def is_sequence(v):
    return isinstance(v, (list, tuple))

def match_sequence(t, p, params):
    if len(p) != len(t):
        return False
    for tt, pp in zip(t, p):
        if not match(tt, pp, params):
            return False
    return True


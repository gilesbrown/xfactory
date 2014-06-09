from itertools import chain


class _PipeComposable(object):

    def __or__(self, rhs):
        return compose(self, rhs)

    def __ror__(self, lhs):
        return compose(lhs, self)


class Composable(_PipeComposable):
    """ Decorate callable to support pipeline creation using the '|'

    The callable is wrapped in a new class (type).  This lets us
    make the object callable with very little overhead by making
    it a staticmethod of the new class.
    """

    def __new__(cls, func):
        type_name = getattr(func, '__name__', str(func))
        type_bases = (cls,)
        type_dict = dict(
            __new__=super(Composable, cls).__new__,
           __call__=staticmethod(func),
           __doc__=getattr(func, '__doc__', None),
           __name__=getattr(func, '__name__', None),
           __module__=getattr(func, '__module__', None),
        )
        return type(type_name, type_bases, type_dict)()

    @classmethod
    def __getattr__(cls, name):
        return getattr(cls.__call__, name)

    @classmethod
    def __functions__(cls):
        return (cls.__call__,)


# helper for flattening when making a pipeline from other pipelines.
def _functions(func):
    return getattr(func, '__functions__', lambda : (func, ))()


def _flattened(*funcs):
    return chain.from_iterable(_functions(func) for func in funcs)


class ComposedFunction(tuple, _PipeComposable):
    """ Composed function.

    Instances of this class are a tuple of functions.

    These functions are called in sequence.  So:
        ComposedFunction(f1, f2)(*args)
    is equivalent to:
        f2(f1(*args))
    """

    def __new__(cls, func, *morefuncs):
        # nested pipelines are flattened so that
        iterable = _flattened(func, *morefuncs)
        return tuple.__new__(cls, iterable)

    def __call__(self, *args):
        res = self[0](*args)
        for func in self[1:]:
            res = func(res)
        return res

    def __functions__(self):
        return self


def composable(func):
    """ Decorator for composable functions """
    return Composable(func)


def compose(*funcs):
    """ Create a ComposedFunction from one or more functions """
    return ComposedFunction(*funcs)

""" Factory functions for extracting from lxml element trees. """

from urlparse import urljoin
from itertools import imap, ifilterfalse, chain
from functools import partial
from operator import is_, methodcaller

from lxml.etree import XPath
from lxml.cssselect import CSSSelector

from .composed import composable

SKIP = object()
skip = partial(is_, SKIP)

base_href = XPath('//base[@href]/@href')



def css(expression):
    return composable(CSSSelector(expression))


def xpath(expression, **kw):
    namespaces = kw.pop('namespaces', None)
    return composable(XPath(expression, namespaces=namespaces))


def iterattr(name, default=SKIP):
    attrgetter = methodcaller('get', name, default)
    def _iterattr(obj):
        return ifilterfalse(skip, imap(attrgetter, obj))
    return _iterattr


def basejoin(func):
    @composable
    def _basejoin(iterable):
        iterator = iter(iterable)
        try:
            first = iterator.next()
        except StopIteration:
            return
        base_url = (base_href(first) + [first.base_url])[0]
        for url in func(chain((first,), iterator)):
            yield urljoin(base_url, url)
    return _basejoin


@composable
def itertext(obj):
    if hasattr(obj, 'itertext'):
        return obj.itertext()
    elif hasattr(obj, 'decode'):
        return (obj.decode('utf-8'),)
    else:
        return chain.from_iterable(itertext(elem) for elem in obj)


# Extractors for common attributes containing URLs
iterhref = basejoin(iterattr('href'))
itersrc = basejoin(iterattr('src'))

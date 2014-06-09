from operator import itemgetter
from lxml import html
from xfactory.etreefactoryfuncs import (xpath, css,
                                        itertext, iterattr, iterhref)

etree_html = """
<html>
  <head>
  </head>
  <body>
    <h1>hi</h1>
    <div id="div1">
      <a href="/1"></a>
      <a href="/2"></a>
    </div>
    <div id="iter_text">This is <span>some </span>text.</div>
    <div id="nbsp">&nbsp;</div>
  </body>
</html>
"""

etree = html.fromstring(etree_html, base_url='http://some.where/')


def test_xpath():
    f = xpath('//h1/text()')
    assert f(etree) == ['hi']


def test_xpath_namespaces():
    ns = {'re': 'http://exslt.org/regular-expressions'}
    f = (xpath('//*[re:test(text(), "SOME", "i")]/text()', namespaces=ns) |
         itertext |
         list)
    assert f(etree) == ['some ']


def test_css():
    f = css('h1')
    assert [e.tag for e in f(etree)] == ['h1']


def test_iterattr():
    f = css('#div1 a') | iterattr('href') | list
    assert f(etree) == ['/1', '/2']


def test_iterattr_default():
    f = css('#div1 a') | iterattr('nosuch', '') | list
    assert f(etree) == ['', '']


def test_iterattr_missing_default():
    f = css('#div1 a') | iterattr('nosuch') | list
    assert f(etree) == []


def test_iterhref():
    f = css('#div1 a') | iterhref | list
    assert f(etree) == ['http://some.where/1', 'http://some.where/2']


def test_iterhref_empty():
    f = css('#nosuch') | iterhref | list
    assert f(etree) == []


def test_itertext():
    select_elem = css('#iter_text')
    extract_text = select_elem | itertext
    chunks = list(extract_text(etree))
    assert chunks == ['This is ', 'some ', 'text.']


def test_itertext_single_element():
    func = css('#iter_text') | itemgetter(0) | itertext | list
    assert func(etree) == ['This is ', 'some ', 'text.']


def test_itertext_stringresult():
    func = xpath('//*[@id="iter_text"]/text()') | itertext | list
    assert func(etree) == ['This is ', 'text.']


def test_itertext_nbsp():
    func = css('#nbsp') | itertext | list
    assert func(etree) == [u'\xa0']

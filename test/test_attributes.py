from xfactory.attributes import Attributes


def test_attributes():
    attributes = Attributes()
    attributes.add('foo', lambda v: v)
    actual = list(attributes('bar'))
    expected = [('foo', 'bar')]
    assert actual == expected


def test_attributes_keywords():
    attributes = Attributes(foo=lambda v: v)
    actual = list(attributes('bar'))
    expected = [('foo', 'bar')]
    assert actual == expected


def test_len():
    attributes = Attributes()
    attributes.add('foo', lambda v: v)
    assert len(attributes) == 1


def test_attribute_add_as_decorator():
    attributes = Attributes()
    @attributes.add
    def foo(value):
        return value
    actual = list(attributes('bar'))
    expected = [('foo', 'bar')]
    assert actual, expected


def test_attribute_generator():
    attributes = Attributes()
    @attributes.add
    def foo(value):
        for character in value:
            yield character
    actual = list(attributes('bar'))
    expected = [('foo', 'b'), ('foo', 'a'), ('foo', 'r'),]
    assert actual == expected


def test_attribute_exception():
    attributes = Attributes()
    @attributes.add
    def foo(value):
        raise ValueError(value)
    actual = list(attributes('bar'))
    assert len(actual) == 1
    actual_name, actual_value = actual[0]
    assert actual_name == 'foo'
    assert isinstance(actual_value, Exception)


def test_attribute_exception_in_generator():
    attributes = Attributes()
    @attributes.add
    def foo(value):
        for i, character in enumerate(value):
            if i > 0:
                raise ValueError(character)
            yield character
        raise ValueError(value)
    actual = list(attributes('bar'))
    assert len(actual) == 2
    # The first value came out ok...
    assert actual[0] == ('foo', 'b')
    actual_name, actual_value = actual[1]
    assert actual_name == 'foo'
    # But the second one is an error.
    assert isinstance(actual_value, Exception)

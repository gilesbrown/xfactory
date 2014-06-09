from xfactory.composed import composable


@composable
def squared(x):
    return x * x


def add_1(x):
    return x + 1


def test_composable():
    func = squared | add_1
    assert func(2) == 5


def test_composable_on_rhs():
    func = int | squared
    assert func('2') == 4


def test_composing_composed():
    func = squared | squared | squared
    assert func(2) == 256

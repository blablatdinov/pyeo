from pyeo import elegant


@elegant
class SomeObject(object):

    def method(self):
        return 5


def test():
    assert SomeObject().method() == 5

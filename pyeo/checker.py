from typing import Type

from typing_extensions import TypeAlias, final


@final
class Checker(object):

    def __init__(self, tree, filename):
        self._tree = tree
        self._filename = filename

    def run(self):
        pass

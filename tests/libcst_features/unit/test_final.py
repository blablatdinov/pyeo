from pyeo.__main__ import main

module = """
from pyeo import elegant
from typing import Protocol

@elegant
class House(Protocol):

    def area(self) -> int: ...

@elegant
class HttpHouse(House):

    def area(self) -> int:
        return 5
"""


def test(tmpdir):
    (tmpdir / 'name.py').write_text(module, encoding='utf-8')
    main(tmpdir / 'name.py')

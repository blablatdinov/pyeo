from pyeo.__main__ import main

module = """
from typing import Protocol

import attrs
from pyeo import elegant

@elegant
class House(Protocol):

    def area(self) -> int: ...

@elegant
@attrs.define(frozen=True)
class HttpHouse(House):

    def area(self) -> int:
        return 5
"""


def test(tmpdir):
    (tmpdir / 'name.py').write_text(module, encoding='utf-8')
    main(tmpdir / 'name.py')

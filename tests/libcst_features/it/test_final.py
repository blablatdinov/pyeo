from typer.testing import CliRunner
from pyeo.__main__ import app

module = """
from typing import Protocol

import attrs
from pyeo import elegant

@elegant
class House(Protocol):

    def area(self) -> int: ...

@attrs.define(frozen=True)
@elegant
class HttpHouse(House):

    def area(self) -> int:
        return 5
"""


def test(tmpdir):
    (tmpdir / 'name.py').write_text(module, encoding='utf-8')
    got = CliRunner().invoke(app, [str(tmpdir / 'name.py')])

    assert got.exit_code == 0
    assert got.stdout.strip() == '14:0 HttpHouse class must be final'

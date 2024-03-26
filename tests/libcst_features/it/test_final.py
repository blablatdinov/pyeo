from typer.testing import CliRunner
from pyeo.__main__ import app

invalid_module = """
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

generic_protocol = """
from typing import Protocol, TypeVar

import attrs
from pyeo import elegant

T = TypeVar('T')

@elegant
class House(Protocol[T]):

    def area(self) -> int: ...
"""


def test(tmpdir):
    (tmpdir / 'name.py').write_text(invalid_module, encoding='utf-8')
    got = CliRunner().invoke(app, [str(tmpdir / 'name.py')])

    assert got.exit_code == 0
    assert got.stdout.strip() == '14:0 HttpHouse class must be final'


def test_generic_protocol(tmpdir):
    (tmpdir / 'name.py').write_text(generic_protocol, encoding='utf-8')
    got = CliRunner().invoke(app, [str(tmpdir / 'name.py')])

    assert got.exit_code == 0
    assert got.stdout.strip() == ''

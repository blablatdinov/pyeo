"""The MIT License (MIT).

Copyright (c) 2023 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
from pathlib import Path

from typer import Typer
import libcst as cst


app = Typer()


def _fullname(name: str, parsed_module):
    for elem in parsed_module.body:
        if isinstance(elem, cst.SimpleStatementLine):
            for body_elem in elem.body:
                if isinstance(body_elem, cst.ImportFrom):
                    module_name = body_elem.module.value
                    for name in body_elem.names:
                        print(module_name, name.name.value)


def _is_elegant_class(elem, parsed_module):
    if isinstance(elem, cst.ClassDef):
        for decorator in elem.decorators:
            _fullname(decorator.decorator.value, parsed_module)


@app.command()
def main(
    path: str,
):
    module = cst.parse_module(Path(path).read_text())
    for elem in module.body:
        _is_elegant_class(elem, module)


if __name__ == '__main__':
    app()

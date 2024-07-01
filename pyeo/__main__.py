# The MIT License (MIT).
#
# Copyright (c) 2023-2024 Almaz Ilaletdinov <a.ilaletdinov@yandex.ru>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

from pathlib import Path

from typer import Typer
import libcst as cst


app = Typer()


class ElegantClassMustBeFinal(Exception): pass


def _fullname(name: str, parsed_module):
    for elem in parsed_module.body:
        if isinstance(elem, cst.SimpleStatementLine):
            for body_elem in elem.body:
                if isinstance(body_elem, cst.ImportFrom):
                    module_name = body_elem.module.value
                    for body_name in body_elem.names:
                        if name == body_name.name.value:
                            return f'{module_name}.{name}'


def _is_elegant_class(elem, parsed_module):
    if not isinstance(elem, cst.ClassDef):
        return
    is_elegant = False
    is_protocol = False
    for decorator in elem.decorators:
        # FIXME: it may be some alias
        #
        # from pyeo import elegant
        # other_name = elegant
        if _fullname(decorator.decorator.value, parsed_module) == 'pyeo.elegant':
            print(_fullname(decorator.decorator.value, parsed_module))
            is_elegant = True
            break
    for base in elem.bases:
        if _fullname(base.value.value, parsed_module) == 'typing.Protocol':
            is_elegant = True
            break
    return is_elegant and not is_protocol


def _process_class(elem, parsed_module) -> list[str]:
    final_finded = False
    for decorator in elem.decorators:
        if isinstance(decorator.decorator, cst.Call):
            continue
        if _fullname(decorator.decorator.value, parsed_module) == 'typing.final':
            final_finded = True
    if not final_finded:
        raise ElegantClassMustBeFinal


def _process_module(path: Path) -> list[str]:
    module = cst.parse_module(Path(path).read_text())
    errors = []
    for elem in module.body:
        if _is_elegant_class(elem, module):
            try:
                _process_class(elem, module)
            except ElegantClassMustBeFinal:
                print(elem.name.value)
                errors.append(
                    f''
                )


@app.command()
def main(
    path: str,
):
    path = Path(path)
    if path.is_dir():
        for path_ in path.glob('**/*.py'):
            _process_module(path_)
    else:
        _process_module(path)


if __name__ == '__main__':
    app()

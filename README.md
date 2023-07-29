# pyeo

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Pyeo  is an advanced static analysis tool tailored specifically to enforce the principles advocated by
Elegant Objects (elegantobjects.org) in Python projects. It serves as a quality control instrument to ensure
that your Python code adheres to the core tenets of elegance, simplicity, and maintainability.

```bash
pip install eo-styleguide
```

Simple example of usage:

```python
from typing import Protocol, final

import attrs
from pyeo import elegant


class House(Protocol):
    def area(self) -> int: ...


@elegant
@final
@attrs.define(frozen=True)
class HttpHouse(House):

    def area(self) -> int:
        return 10
```

- [x] ~~No null~~ ([why?](http://www.yegor256.com/2014/05/13/why-null-is-bad.html))

Mypy helps prevent AttributeError and other type-related errors by providing static type checking for Python code. It allows specifying variable types, function arguments, and return types to catch potential type issues before the program runs. By using Mypy, developers can identify and fix problems related to attribute access and other type mismatches, leading to improved code quality and easier maintenance.

- [x] No code in constructors ([why?](http://www.yegor256.com/2015/05/07/ctors-must-be-code-free.html))

- [x] No getters and setters ([why?](http://www.yegor256.com/2014/09/16/getters-and-setters-are-evil.html))

- [x] No mutable objects ([why?](http://www.yegor256.com/2014/06/09/objects-should-be-immutable.html))

`attrs.define(frozen=True)` is a parameter used in the attrs library to create classes with attributes that cannot be modified after the instance is created (i.e., immutable or "frozen" classes).
The [attrs](https://www.attrs.org/en/stable/) library allows defining classes using the `@attr.s` decorator or by explicitly calling the `attr.define` function, and `frozen=True` is one of the parameters for specifying attribute behavior in the class. 
When you use `attrs.define(frozen=True)` for a class, all its attributes become read-only after the instance is created, making the class "frozen" or "immutable," preventing any changes to its attribute values.

- [x] No readers, parsers, controllers, sorters, and so on ([why?](https://www.yegor256.com/2015/03/09/objects-end-with-er.html))

- [x] No static methods, not even private ones ([why?](http://www.yegor256.com/2017/02/07/private-method-is-new-class.html))

- [x] No instanceof, type casting, or reflection ([why?](http://www.yegor256.com/2015/04/02/class-casting-is-anti-pattern.html))

- [x] No public methods without a contract (interface) ([why?](https://www.yegor256.com/2014/11/20/seven-virtues-of-good-object.html#2-he-works-by-contracts))

- [ ] No statements in test methods except assert ([why?](http://www.yegor256.com/2017/05/17/single-statement-unit-tests.html))

- [ ] No ORM or ActiveRecord ([why?](https://www.yegor256.com/2014/12/01/orm-offensive-anti-pattern.html) and [why?](https://www.yegor256.com/2016/07/26/active-record.html))

Detect using ORM or ActiveRecord tools on project by design/code review

- [x] No implementation inheritance ([why?](http://www.yegor256.com/2017/01/31/decorating-envelopes.html) and [why?](http://www.yegor256.com/2016/09/13/inheritance-is-procedural.html))

Each `@elegant` object must be `typing.final`

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

## Contents
- Principles
  - [No null](#no-null) ([why?](http://www.yegor256.com/2014/05/13/why-null-is-bad.html)
  - [No code in constructors](#no-code-in-constructors) ([why?](http://www.yegor256.com/2014/05/13/why-null-is-bad.html))

  - [No getters and setters](#no-getters-and-setters) ([why?](http://www.yegor256.com/2014/09/16/getters-and-setters-are-evil.html))
 
  - [No mutable objects](#no-mutable-objects) ([why?](http://www.yegor256.com/2014/06/09/objects-should-be-immutable.html))

  - [No readers, parsers, controllers, sorters, and so on](#no-er-suffix) ([why?](https://www.yegor256.com/2015/03/09/objects-end-with-er.html))

  - [No static methods, not even private ones](no-static-methods) ([why?](http://www.yegor256.com/2017/02/07/private-method-is-new-class.html))

  - [No instanceof, type casting, or reflection](no-reflection) ([why?](http://www.yegor256.com/2015/04/02/class-casting-is-anti-pattern.html))

  - [No public methods without a contract (interface)](#no-public-methods-without-a-contract) ([why?](https://www.yegor256.com/2014/11/20/seven-virtues-of-good-object.html#2-he-works-by-contracts))

  - [No statements in test methods except assert](#no-statements-in-tests) ([why?](http://www.yegor256.com/2017/05/17/single-statement-unit-tests.html))

  - [No ORM or ActiveRecord](#no-orm) ([why?](https://www.yegor256.com/2014/12/01/orm-offensive-anti-pattern.html) and [why?](https://www.yegor256.com/2016/07/26/active-record.html))

  - [No implementation inheritance](#no-inheritance) ([why?](http://www.yegor256.com/2017/01/31/decorating-envelopes.html) and [why?](http://www.yegor256.com/2016/09/13/inheritance-is-procedural.html))

## No null

Mypy helps prevent `AttributeError`` and other type-related errors by providing static type checking for Python code. It allows specifying variable types, function arguments, and return types to catch potential type issues before the program runs. By using Mypy, developers can identify and fix problems related to attribute access and other type mismatches, leading to improved code quality and easier maintenance.

Example:

```python
class Employee(object):
    def __init__(self, user_id: int):
        self._user_id = user_id

def get_by_id(user_id: int) -> Employee:
    if user_id < 0:
        return None
    return Employee(user_id)
```

Mypy return next violation:

```
error: Incompatible return value type (got "None", expected "Employee")  [return-value]
```

So, we must use `typing.Optional` or `|` (union) operator.

It's works:

```
def get_by_id(user_id: int) -> Optional[Employee]: ...
def get_by_id(user_id: int) -> Employee | None: ...
```

## No code in constructors

You can use `@attrs.define` for skip this. It decorator create ctor for your classes automatically. However, we implement check that your primary and secondary ctors not contain code, with the exception of attributes assingment. Please check [NoCodeInCtorFeature](/pyeo/features/no_code_in_ctors.py).

## No getters and setters

Actually we realize functional for to prohibit the use of `@property` and `@setter` method decorators. You can use `@attrs.define(frozen=True)` in order to make an object immutable.

Prohibit the use of `@property` decorator not protect from evil of getters, so if you can ideas how we can implement more complex check, create issue please.

## No mutable objects

`attrs.define(frozen=True)` is a parameter used in the attrs library to create classes with attributes that cannot be modified after the instance is created (i.e., immutable or "frozen" classes).
The [attrs](https://www.attrs.org/en/stable/) library allows defining classes using the `@attr.s` decorator or by explicitly calling the `attr.define` function, and `frozen=True` is one of the parameters for specifying attribute behavior in the class. 
When you use `attrs.define(frozen=True)` for a class, all its attributes become read-only after the instance is created, making the class "frozen" or "immutable," preventing any changes to its attribute values.

## No er suffix

We check you class name not contain `-er` or `(C|c)lient` suffix by check in [NoErNamesFeature](/pyeo/features/no_er_names.py)

## No static methods

Check by [NoStaticmethodsFeature](/pyeo/features/no_staticmethods.py)

## No reflection

Prohibit next function calls:
- `isinstance`
- `type`
- `issubclass`
- `hasattr`

## No public methods without a contract

In Python, `typing.Protocol` is a class introduced in Python 3.8 as part of the typing module. It is used to define structural subtyping or "duck typing" for classes, which allows you to create interfaces without using explicit inheritance.

[EachMethodHasProtocolFeature](/pyeo/features/method_has_protocol.py) rule check that all of public class methods has protocol.

## No statements in tests

TODO

## No ORM

Detect using ORM or ActiveRecord tools on project by design/code review

## No inheritance

Each `@elegant` object must be `typing.final`. Check by [FinalClassFeature](/pyeo/features/final_object.py)

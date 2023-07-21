# pyeo

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Pyeo  is an advanced static analysis tool tailored specifically to enforce the principles advocated by
Elegant Objects (elegantobjects.org) in Python projects. It serves as a quality control instrument to ensure
that your Python code adheres to the core tenets of elegance, simplicity, and maintainability.

- No null ([why?](http://www.yegor256.com/2014/05/13/why-null-is-bad.html))
- No code in constructors ([why?](http://www.yegor256.com/2015/05/07/ctors-must-be-code-free.html))
- No getters and setters ([why?](http://www.yegor256.com/2014/09/16/getters-and-setters-are-evil.html))
- No mutable objects ([why?](http://www.yegor256.com/2014/06/09/objects-should-be-immutable.html))
- No readers, parsers, controllers, sorters, and so on ([why?](https://www.yegor256.com/2015/03/09/objects-end-with-er.html))
- No static methods, not even private ones ([why?](http://www.yegor256.com/2017/02/07/private-method-is-new-class.html))
- No instanceof, type casting, or reflection ([why?](http://www.yegor256.com/2015/04/02/class-casting-is-anti-pattern.html))
- No public methods without a contract (interface) ([why?](https://www.yegor256.com/2014/11/20/seven-virtues-of-good-object.html#2-he-works-by-contracts))
- No statements in test methods except assertThat ([why?](http://www.yegor256.com/2017/05/17/single-statement-unit-tests.html))
- No ORM or ActiveRecord ([why?](https://www.yegor256.com/2014/12/01/orm-offensive-anti-pattern.html) and [why?](https://www.yegor256.com/2016/07/26/active-record.html))
- No implementation inheritance ([why?](http://www.yegor256.com/2017/01/31/decorating-envelopes.html) and [why?](http://www.yegor256.com/2016/09/13/inheritance-is-procedural.html))

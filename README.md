## WHAT & WHY

Extending Python's Future (Promise) object with missing chaining API like `.then()` and others.

While Futures (aka Promises) [are formally specified and available](https://www.python.org/dev/peps/pep-3148/) as part of Python as of v 3.2+,
and is available as [backported module for Python versions v.2.x](https://pypi.python.org/pypi/futures),
formal, standard implementation is lacking any formal or convenient API for the most frequent use of Promises - chaining.

[JavaScript Promises](https://github.com/promises-aplus/promises-spec) have then-ability as part of the spec.
This extension of Python Future object borrows `.then()` behavior from [JavaScript Promises](https://github.com/promises-aplus/promises-spec).


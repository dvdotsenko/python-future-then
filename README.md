## WHAT & WHY

Extending Python's Future (Promise) object with missing chaining API like `.then()` and others.

While Futures (aka Promises) [are formally specified and available](https://www.python.org/dev/peps/pep-3148/) as part of Python as of v 3.2+,
and is available as [backported module for Python versions v.2.x](https://pypi.python.org/pypi/futures),
formal, standard implementation is lacking any formal or convenient API for the most frequent use of Promises - chaining.

[JavaScript Promises](https://github.com/promises-aplus/promises-spec) have then-ability as part of the spec.
This extension of Python Future object borrows `.then()` behavior from [JavaScript Promises](https://github.com/promises-aplus/promises-spec).

## INSTALL

`pip install futures_then`

## USE

```python
In [1]: from futures_then import ThenableFuture as Future

In [2]: f1 = Future()

In [3]: f2 = f1.then(lambda v: v + ' transformed')

In [4]: f1.set_result('future')

In [5]: f2.result()
Out[5]: 'future transformed'
```

# cloudpickle

`cloudpickle` makes it possible to serialize Python constructs not supported
by the default `pickle` module from the Python standard library.

`cloudpickle` is especially useful for **cluster computing** where Python
code is shipped over the network to execute on remote hosts, possibly close
to the data.

Among other things, `cloudpickle` supports pickling for **lambda functions**
along with **functions and classes defined interactively** in the
`__main__` module (for instance in a script, a shell or a Jupyter notebook).

Cloudpickle can only be used to send objects between the **exact same version
of Python**.

Using `cloudpickle` for **long-term object storage is not supported and
strongly discouraged.**

**Security notice**: one should **only load pickle data from trusted sources** as
otherwise `pickle.load` can lead to arbitrary code execution resulting in a critical
security vulnerability.

Examples
--------

Pickling a lambda expression:

```python
>>> import cloudpickle
>>> squared = lambda x: x ** 2
>>> pickled_lambda = cloudpickle.dumps(squared)

>>> import pickle
>>> new_squared = pickle.loads(pickled_lambda)
>>> new_squared(2)
4
```

Pickling a function interactively defined in a Python shell session
(in the `__main__` module):

```python
>>> CONSTANT = 42
>>> def my_function(data: int) -> int:
...     return data + CONSTANT
...
>>> pickled_function = cloudpickle.dumps(my_function)
>>> depickled_function = pickle.loads(pickled_function)
>>> depickled_function
<function __main__.my_function(data:int) -> int>
>>> depickled_function(43)
85
```

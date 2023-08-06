📦 perfect-eval
=======================

Safe eval module

Installation
-----

```bash
pip install -i https://mirrors.aliyun.com/pypi/simple/ --extra-index-url https://pypi.org/simple/ perfect-eval
```

Example
-----

```python
from perfect_eval import eval_expr

eval_expr("print('hello world')", {"print": print})
# output: hello world
print(eval_expr("now.strftime('%m-%d')", {"now": datetime.now()}))
# output: 10-31
print(eval_expr("a + b", {"a": 123, "b": 456}))
# output: 579
print(eval_expr("f'{a} + {b} = {a + b}'", {"a": 123, "b": 456}))
# output: 123 + 456 = 579
print(eval_expr("match(a, [(1, '11'), (2, '22'), (3, '33')], default='ooo')", {"a": 1}))
# output: 11
```

To Do
-----

- Be the best version of you.

More Resources
--------------

- [perfect-eval] on github.com
- [Official Python Packaging User Guide](https://packaging.python.org)
- [The Hitchhiker's Guide to Packaging]
- [Cookiecutter template for a Python package]

License
-------

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

[version-handle]: https://github.com/holbos-deng/version-handle

[PyPi]: https://docs.python.org/3/distutils/packageindex.html

[Twine]: https://pypi.python.org/pypi/twine

[image]: https://farm1.staticflickr.com/628/33173824932_58add34581_k_d.jpg

[What is setup.py?]: https://stackoverflow.com/questions/1471994/what-is-setup-py

[The Hitchhiker's Guide to Packaging]: https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html

[Cookiecutter template for a Python package]: https://github.com/audreyr/cookiecutter-pypackage

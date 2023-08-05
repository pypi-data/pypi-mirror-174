MkDocs for PAC
====================

This Package is a MkDocs plugin for the PAC (Point and Click) game engine.
It's generates the LUA docs from lua.cpp.

Build
-----

```bash
python3 -m pip install --upgrade build
python3 -m build
```

Install
-------

```bash
py -m pip install dist/mkdocstrings_pac-0.0.0-py3-none-any.whl --force-reinstall
```

For development
---------------

```bash
python3 -m build && py -m pip install dist/mkdocstrings_pac-0.0.0-py3-none-any.whl --force-reinstall
```

More docs
---------

<https://packaging.python.org/en/latest/tutorials/packaging-projects/>

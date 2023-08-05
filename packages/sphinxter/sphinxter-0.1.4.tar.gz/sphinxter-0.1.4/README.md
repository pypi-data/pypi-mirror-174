sphinxter
=========

Autodoc converting YAML docstrings and code comments to sphinx documentation

Formatting
----------

I wanted something that generated readable HTML documentation from readable Code documentation.

Even if you've done nothing to your code to use sphinxter, it'll generate decent documentation assuming non YAML
docstrings are descriptions for their resources.

Say this is yourmodule

```python
"""
The module description
"""

foo = None # The foo description

def func(
    bar:int # The bar description
)->bool:
    """
    The function description
    """
```

This would be the result in `docs/source/index.rst`:

```rst
.. created by sphinxter
.. default-domain:: py

yourmodule
==========

.. module:: yourmodule

The module description

.. attribute:: foo

    The foo description

.. function:: func(bar: int)

    The function description

    :param bar: The bar description
    :type bar: int
    :rtype: bool
```

Not only is this decent documentation, sphinxter picked up the comments next to both attributes and function parameters,
which is a very common, readable pattern in code.

Another useful couple of features is that sphinxter can read dosctrings as YAML and it can read attributes docstrings
(which yes, don't really exist, but it works anyway) allowing for some complex but still readable behavior.

Say this is yourmodule now:

```python
"""
The module description
"""

foo = None # The foo description
"""
usage: |
    Do it this way::

        yourmodule.foo = 7
"""

def func(
    bar:int # The bar description
)->bool:
    """
    description: The function description
    return: Whether the function worked or not
    """
```

This would now be the result in `docs/source/index.rst`:

```rst
.. created by sphinxter
.. default-domain:: py

yourmodule
==========

.. module:: yourmodule

The module description

.. attribute:: foo

    The foo description

    **Usage**

    Do it this way::

        yourmodule.foo = 7

.. function:: func(bar: int)

    The function description

    :param bar: The bar description
    :type bar: int
    :return: Whether the function worked or not
    :rtype: bool
```

Taking advantage of attribute docstrings and YAML docstrings added more documentation, but didn't really lessen
the readability of the code.

That's the goal of sphinxter.

Organization
------------

By default, everything ends up in the `index.rst` document. With modules, classes, and functions you can a different
document and even the order in which they'll appear in the document. If the parent modules don't match, sphinxter will
add a currentmodule directive so everything will be organized properly.

Setup
-----

To setup a package to use sphinxter:

1. Install sphinxter (which includes sphinx)

```
    pip install sphinxter
```

2. Setup documentation area as `docs/source`:

```
    sphinx-quickstart docs --sep -p yourmodule -a 'Your Name' -r yourversion -l en
```

3. Create a script `docs.py` like so:

```
    #!/usr/bin/env python

    import sphinxter
    import yourmodule

    sphinxter.Sphinxter(yourmodule).process()
```

4. Run that script to auto generate docs from your docstrings (they'll end up in `docs/source`):

```
    chmod a+x docs.py
    ./docs.py
```

5. Create HTML from those documents (they'll end up in `docs/build/html`):

```
    sphinx-build -b html docs/source/ docs/build/html
```

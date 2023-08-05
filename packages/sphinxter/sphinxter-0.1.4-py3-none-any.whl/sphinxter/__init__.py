"""
description: |
    Autodoc converting YAML docstrings and code comments to sphinx documentation

    Formatting
    ----------

    I wanted something that generated readable HTML documentation from readable Code documentation.

    Even if you've done nothing to your code to use sphinxter, it'll generate decent documentation assuming non YAML
    docstrings are descriptions for their resources.

    Say this is yourmodule::

        \"""
        The module description
        \"""

        foo = None # The foo description

        def func(
            bar:int # The bar description
        )->bool:
            \"""
            The function description
            \"""

    This would be the result in `docs/source/index.rst`::

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

    Not only is this decent documentation, sphinxter picked up the comments next to both attributes and function parameters,
    which is a very common, readable pattern in code.

    Another useful couple of features is that sphinxter can read dosctrings as YAML and it can read attributes docstrings
    (which yes, don't really exist, but it works anyway) allowing for some complex but still readable behavior.

    Say this is yourmodule now::

        \"""
        The module description
        \"""

        foo = None # The foo description
        \"""
        usage: |
            Do it this way::

                yourmodule.foo = 7
        \"""

        def func(
            bar:int # The bar description
        )->bool:
            \"""
            description: The function description
            return: Whether the function worked or not
            \"""

    This would now be the result in `docs/source/index.rst`::

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

    Taking advantage of attribute docstrings and YAML docstrings added more documentation, but didn't really lessen
    the readability of the code.

    That's the goal of sphinxter.

    * To see how functions are read and written, check out :any:`Reader.routine()` and :any:`Writer.function()` respectively

    * To see how classes are read and written, check out :any:`Reader.cls()` and :any:`Writer.cls()` respectively

    * To see how methods are read and written, check out :any:`Reader.routine()` and :any:`Writer.method()` respectively

    * To see how modules are read and written, check out :any:`Reader.module()` and :any:`Writer.module()` respectively

    Organization
    ------------

    By default, everything ends up in the `index.rst` document. With modules, classes, and functions you can a different
    document and even the order in which they'll appear in the document. Sphinxter will add a currentmodule directive as
    resources are written and the paretn changes so everything will be organized properly.

    * To see how and where to place resource content, check out :any:`Sphinxter.document()`

    * To see how documents store resource content, check out :any:`Document.contents`

    Setup
    -----

    To setup a package to use sphinxter:

    #. Install sphinxter (which includes sphinx)::

        pip install sphinxter

    #. Setup documentation area as `docs/source`::

        sphinx-quickstart docs --sep -p yourmodule -a 'Your Name' -r yourversion -l en

    #. Create a script `docs.py` like so::

        #!/usr/bin/env python

        import sphinxter
        import yourmodule

        sphinxter.Sphinxter(yourmodule).process()

    #. Run that script to auto generate docs from your docstrings (they'll end up in `docs/source`)::

        chmod a+x docs.py
        ./docs.py

    #. Create HTML from those documents (they'll end up in `docs/build/html`)::

        sphinx-build -b html docs/source/ docs/build/html

    * To change settings, like docs location, indenting by, check out :any:`sphinxter.Sphinxter`
"""

from sphinxter.reader import Reader
from sphinxter.document import Document
from sphinxter.writer import Writer

class Sphinxter:
    """
    description: Class for reading documentation and writing into documents
    document: sphinxter
    """

    modules = None      # list of modules to read
    titles = None       # hash of titles, keyed by document name
    toctree = None      # main toctree list of document names, default: ['*', 'self']
    base = None         # base directory to write documents
    indent = None       # string to use for indenting
    documents = None    # hash of documents, keyed by name

    def __init__(self,
        modules:'module or list[module]',   # module or modules to read
        titles:dict=None,                   # document titles to use
        toctree:dict=None,                  # list of document names to use for the main toctree
        base:str="docs/source",             # base directory to store generated documents
        indent:str='    '                   # string to use for indenting
    ):

        if not isinstance(modules, list):
            modules = [modules]

        self.modules = modules
        self.titles = titles if titles is not None else {}
        self.toctree = toctree if toctree is not None else ['self', '*']
        self.base = base
        self.indent = indent
        self.documents = {}

    def document(self,
        module:str,         # resource's parent module's name
        kind:str,           # resource's kind, module, function, or class
        parsed:dict,        # resource's parsed documentation
        current:str='index' # the last document named
    ):
        """
        description: Adds a resource's documentation to its document
        usage: |
            You can specify a resource's document and order in that document
            with a `document` directive in the YAML::

                def func():
                    \"""
                    document:
                        path: different
                        order: 10
                    \"""

                # {
                #     "path": "different",
                #     "order": 10
                # }

            This would place the func function in the different.rst document with all
            the other resources at the 10 posiiton.

            If you only specify document as a `str`, it assume you meant path and
            that order is 0::

                def func():
                    \"""
                    document: different
                    \"""

                # {
                #     "path": "different",
                #     "order": 0
                # }

            If you only specify document as an `int`, it assume you meant order and
            that the path hasn't changed::

                def func():
                    \"""
                    document: 10
                    \"""

                # {
                #     "path": "index",
                #     "order": 10
                # }
        """

        document = parsed.get("document", {})

        if isinstance(document, bool) and not document:
            return current

        if isinstance(document, str):
            document = {"path": document}

        if isinstance(document, int):
            document = {"order": document}

        path = document.get("path", current)
        order = document.get("order", 0)

        if path not in self.documents:

            if path != 'index':
                title = self.titles.get(path, path)
                toctree = False
            else:
                title = self.titles.get(path, module)
                toctree = self.toctree

            self.documents[path] = Document(f"{self.base}/{path}.rst", title, toctree, self.indent)

        self.documents[path].add(module, kind, parsed, order)

        return path

    def read(self):
        """
        Reads all the documentation into their document(s)
        """

        for module in self.modules:

            parsed = Reader.module(module)

            path = self.document(parsed['name'], "module", parsed)

            for function in parsed["functions"]:
                self.document(parsed['name'], "function", function, path)

            for cls in parsed["classes"]:
                self.document(parsed['name'], "class", cls, path)

            for cls in parsed["exceptions"]:
                self.document(parsed['name'], "exception", cls, path)

    def write(self):
        """
        Writes all document(s)
        """

        for document in self.documents.values():
            with open(document.path, "w", encoding="utf-8") as file:
                Writer(document, file).dump()

    def process(self):
        """
        Reads module(s) and writes document(s) end to end
        """

        self.read()
        self.write()

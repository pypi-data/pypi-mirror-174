"""
Module for writing out documents
"""

# pylint: disable=too-many-lines

class Writer:
    """
    description: Class for writing out documents (rst)
    document: writer
    """

    document = None # document object to write out
    file = None     # file handle to write out to

    def __init__(self,
        document:'sphinxter.Document',  # document object to write out
        file                            # file handle like object to write to
    ):

        self.document = document
        self.file = file

    def line(self,
        line:str='',        # Text to write out
        indent:int=0,       # How many times to indent
        before:bool=False,  # Whether to put a blankline before
        after:bool=False    # Whether to put a blankline after
    ):
        """
        description: Writes a line of text to the filehandle
        usage: |
            This can just write a line of text::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.line("Hello, world!")
                handle.getvalue()
                # Hello, world!
                #

            It can indent::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.line("Hello, world!", indent=1)
                handle.getvalue()
                #     Hello, world!
                #

            And it can add lines (with no indent) before and after::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.line("Hello, world!", indent=1, before=True, after=True)
                handle.getvalue()
                #
                #     Hello, world!
                #
                #
        """

        if before:
            self.file.write("\n")

        self.file.write(f"{self.document.indent * indent}{line}".rstrip())

        self.file.write("\n")

        if after:
            self.file.write("\n")

    def lines(self,
        lines:str,          # Multil\ine text to write out
        indent:int  ,       # How many times to indent
        before:bool=False,  # Whether to put a blankline before
        after:bool=False    # Whether to put a blankline after
    ):
        """
        description: Writes lines of text to the filehandle
        usage: |
            This can just write lines of text::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.lines("Hello\\nworld!", indent=0)
                handle.getvalue()
                # Hello
                # world!
                #

            It can indent::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.lines("Hello\\nworld!", indent=1)
                handle.getvalue()
                #     Hello
                #     world!
                #

            And it can add lines (with no indent) before and after::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.lines("Hello\\nworld!", indent=1, before=True, after=True)
                handle.getvalue()
                #
                #     Hello
                #     world!
                #
                #
        """

        if before:
            self.file.write("\n")

        for line in lines.split("\n"):
            self.line(line, indent)

        if after:
            self.file.write("\n")

    @staticmethod
    def types(
        types:'str or list' # Type(s) to write out
    ):
        """
        description: Takes a str of type or list of str of type and returns a str
        usage: |
            If just a single type, it returns that::

                import sphinxter

                sphinxter.Writer.types("str")
                # "str"

            If a list of types, return types, concatenated with ' or '::

                sphinxter.Writer.types(["str", "list"])
                # "str or list"
        """

        if not isinstance(types, list):
            types = [types]

        return " or ".join(types)

    def description(self,
        parsed:dict,    # parsed documentation
        indent:int      # amount to indent by
    ):
        """
        description: Writes description if present, preceeding with a blank line
        usage: |

            If there's a description in the documentation, it writes it out with a preceeding blank line::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "description": "It is what it is"
                }

                writer.description(parsed, indent=1)
                handle.getvalue()
                #
                #     It is what it is
                #

            If there's no description, it does nothing::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {}

                writer.description(parsed, indent=1)
                handle.getvalue()
                #
        """

        if "description" not in parsed:
            return

        self.lines(parsed["description"].rstrip(), indent, before=True)

    def parameter(self,
        parsed:dict,    # parsed documentation for a parameter
        indent:int      # amount to indent by
    ):
        """
        description: Writes parameter documentation
        usage: |

            If there's only a name::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "name": "arg"
                }

                writer.parameter(parsed, indent=1)
                handle.getvalue()
                #     :param arg:
                #

            If there's also a description::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "name": "arg",
                    "description": "an argument"
                }

                writer.parameter(parsed, indent=1)
                handle.getvalue()
                #     :param arg: an argument
                #

            If there's also a type::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "name": "arg",
                    "description": "an argument",
                    "type": "bool"
                }

                writer.parameter(parsed, indent=1)
                handle.getvalue()
                #     :param arg: an argument
                #     :type arg: bool
                #
        """

        if "description" in parsed:
            self.line(f":param {parsed['name']}: {parsed['description']}", indent)
        else:
            self.line(f":param {parsed['name']}:", indent)

        if "type" in parsed:
            self.line(f":type {parsed['name']}: {self.types(parsed['type'])}", indent)

    def parameters(self,
        parsed:dict,    # parsed documentation possibly keyed by parameters
        indent:int      # amount to indent by
    ):
        """
        description: Writes parameters if present
        usage: |
            If parameters are present, write them::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "parameters": [
                        {
                            "name": "small"
                        },
                        {
                            "name": "big",
                            "description": "stuff",
                            "type": "int"
                        }
                    ]
                }

                writer.parameters(parsed, 1)
                handle.getvalue()
                #     :param small:
                #     :param big: stuff
                #     :type big: int
                #

            If not, do nothing::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {}

                writer.parameters(parsed, 1)
                handle.getvalue()
                #
        """

        if "parameters" not in parsed:
            return

        for parameter in parsed["parameters"]:
            self.parameter(parameter, indent)

    def returns(self,
        parsed:dict,    # parsed documentation possibly keyed by return
        indent:int      # amount to indent by
    ):
        """
        description: Writes return information if present
        usage: |
            If there's a description::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "return": {
                        "description": "stuff"
                    }
                }

                writer.returns(parsed, 1)
                handle.getvalue()
                #     :return: stuff
                #

            If there's also a type::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "return": {
                        "description": "stuff",
                        "type": "int"
                    }
                }

                writer.returns(parsed, 1)
                handle.getvalue()
                #     :return: stuff
                #     :rtype: int
                #

            If there's only a type::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "return": {
                        "type": "int"
                    }
                }

                writer.returns(parsed, 1)
                handle.getvalue()
                #     :rtype: int
                #

            If there's nothing, do nothing::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {}

                writer.returns(parsed, 1)
                handle.getvalue()
                #
        """

        if "return" not in parsed:
            return

        if "description" in parsed['return']:
            self.line(f":return: {parsed['return']['description']}", indent)

        if "type" in parsed['return']:
            self.line(f":rtype: {self.types(parsed['return']['type'])}", indent)

    def raises(self,
        parsed:dict,    # parsed documentation possibly keyed by raises
        indent:int      # amount to indent by
    ):
        """
        description: Writes raises information if present
        usage: |
            If there's raises, write them (alphabetically)::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "raises": {
                        "Exception": "whoops",
                        "Error": "oh no"
                    }
                }

                writer.raises(parsed, 1)
                handle.getvalue()
                #     :raises Error: oh no
                #     :raises Exception: whoops
                #

            If there's nothing, do nothing::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {}

                writer.raises(parsed, 1)
                handle.getvalue()
                #
        """

        if "raises" not in parsed:
            return

        for exception in sorted(parsed["raises"].keys()):
            self.line(f":raises {exception}: {parsed['raises'][exception]}", indent)

    def routine(self,
        parsed:dict,    # parsed documentation possibly keyed by parameters, return, and/or raises
        indent:int      # amount to indent by
    ):
        """
        description: Writes documentation for that which can be excuted
        usage: |
            If there's parameters, return, and/or raises, write them, preceeding by a blank line::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "parameters": [
                        {
                            "name": "small"
                        },
                        {
                            "name": "big",
                            "description": "stuff",
                            "type": "int"
                        }
                    ],
                    "return": {
                        "description": "stuff",
                        "type": "int"
                    },
                    "raises": {
                        "Exception": "whoops",
                        "Error": "oh no"
                    }
                }

                writer.routine(parsed, 1)
                handle.getvalue()
                #
                #     :param small:
                #     :param big: stuff
                #     :type big: int
                #     :return: stuff
                #     :rtype: int
                #     :raises Error: oh no
                #     :raises Exception: whoops
                #

            If there's nothing, do nothing::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {}

                writer.routine(parsed, 1)
                handle.getvalue()
                #
        """

        if (
            "parameters" not in parsed and
            "return" not in parsed and
            "raises" not in parsed
        ):
            return

        self.line()
        self.parameters(parsed, indent)
        self.returns(parsed, indent)
        self.raises(parsed, indent)

    def usage(self,
        parsed:dict,    # parsed documentation possibly keyed by usage
        indent:int      # amount to indent by
    ):
        """
        description: Writes a usage block if present
        usage: |
            If there's usages, write with a header and proper blank lines::

                import io
                import yaml
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                def example():
                    \"""
                    usage: |
                        Here's a neat trick::

                            print("Hello, world!")

                        Cool, huh?
                    \"""

                parsed = yaml.safe_load(example.__doc__)
                # {
                #     "usage": "Here's a neat trick::\\n\\n    print(\\"Hello, world!\\")\\n\\nCool, huh?\\n"
                # }

                writer.usage(parsed, 1)
                handle.getvalue()
                #
                #     **Usage**
                #
                #     Here's a neat trick::
                #
                #         print("Hello, world!")
                #
                #     Cool, huh?
                #

            If there's nothing, do nothing::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {}

                writer.usage(parsed, 1)
                handle.getvalue()
                #
        """

        if "usage" not in parsed:
            return

        self.line("**Usage**", indent, before=True, after=True)
        self.lines(parsed["usage"].rstrip(), indent)

    def function(self,
        parsed:dict,    # entire parsed documentation for a function
        indent:int=0    # amount to indent by
    ):
        """
        description: Writes function content as from :any:`Reader.routine`
        usage: |
            Given the following function as part of the test.example module::

                def func(
                    a:int,   # The a
                    b:'str', # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    \"""
                    description: Some basic func
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return:
                        description: things
                        type:
                        - str
                        - None
                    raises:
                        Exception: if oh noes
                    usage: |
                        Do some cool stuff::

                            like this

                        It's great
                    \"""

            Generating the docs is easy as::

                import io
                import inspect
                import sphinxter
                import test.example

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = sphinxter.Reader.routine(inspect.getattr_static(test.example, 'func'))
                # {
                #     "name": "func",
                #     "kind": "function",
                #     "description": "Some basic func",
                #     "signature": "(a: int, b: 'str', *args, **kwargs)",
                #     "parameters": [
                #         {
                #             "name": "a",
                #             "description": "The a More stuff",
                #             "type": "int"
                #         },
                #         {
                #             "name": "b",
                #             "description": "The b",
                #             "more": "stuff",
                #             "type": "str"
                #         },
                #         {
                #             "name": "args"
                #         },
                #         {
                #             "name": "kwargs",
                #             "a": 1,
                #             "b": 2
                #         }
                #     ],
                #     "return": {
                #         "description": "things",
                #         "type": [
                #             'str',
                #             'None'
                #         ]
                #     },
                #     "raises": {
                #         "Exception": "if oh noes"
                #     },
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                # }

                writer.function(parsed, indent=1)
                handle.getvalue()
                #
                #     .. function:: func(a: int, b: 'str', *args, **kwargs)
                #
                #         Some basic func
                #
                #         :param a: The a More stuff
                #         :type a: int
                #         :param b: The b
                #         :type b: str
                #         :param args:
                #         :param kwargs:
                #         :return: things
                #         :rtype: str or None
                #         :raises Exception: if oh noes
                #
                #         **Usage**
                #
                #         Do some cool stuff::
                #
                #             like this
                #
                #         It's great
                #
        """

        self.line(f".. function:: {parsed['name']}{parsed['signature']}", indent, before=True)

        self.description(parsed, indent+1)
        self.routine(parsed, indent+1)
        self.usage(parsed, indent+1)

    def attribute(self,
        parsed:dict,    # parsed documentation for an attribute
        indent:int      # amount to indent by
    ):
        """
        description: Writes attribute content, preceeded by a blank line
        usage: |
            If there's just a name::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "name": "small"
                }

                writer.attribute(parsed, 1)
                handle.getvalue()
                #
                #     .. attribute:: small
                #

            If there's a description and type::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "name": "big",
                    "description": "stuff",
                    "type": "int"
                }

                writer.attribute(parsed, 1)
                handle.getvalue()
                #
                #     .. attribute:: big
                #         :type: int
                #
                #         stuff
                #
        """

        self.line(f".. attribute:: {parsed['name']}", indent, before=True)

        if "type" in parsed:
            self.line(f":type: {self.types(parsed['type'])}", indent+1)

        self.description(parsed, indent+1)

    def attributes(self,
        parsed:dict,    # parsed documentation possibly containing attributes
        indent:int      # amount to indent by
    ):
        """
        description: Writes attributes content if present
        usage: |
            If there's attributes::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {
                    "attributes": [
                        {
                            "name": "small"
                        },
                        {
                            "name": "big",
                            "description": "stuff",
                            "type": "int"
                        }
                    ]
                }

                writer.attributes(parsed, indent=1)
                handle.getvalue()
                #
                #     .. attribute:: small
                #
                #     .. attribute:: big
                #         :type: int
                #
                #         stuff
                #

            If there's nothing, do nothing::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {}

                writer.attributes(parsed, 1)
                handle.getvalue()
                #
        """
        if "attributes" not in parsed:
            return

        for attribute in parsed["attributes"]:
            self.attribute(attribute, indent)

    def method(self,
        parsed:dict,    # entire parsed documentation for a method
        indent:int      # amount to indent by
    ):
        """
        description: Writes method content as from :any:`Reader.routine`
        usage: |
            For a regular method, assuming the Complex class as part of the test.example module::

                class Complex:

                    @staticmethod
                    def stat(
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    )->list:
                        \"""
                        description: Some static stat
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return: things
                        \"""

                    @classmethod
                    def classy(
                        cls,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some class meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type: str
                        \"""

                    def meth(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some basic meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type:
                            - str
                            - None
                        raises:
                            Exception: if oh noes
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

            Generating docs for a static method::

                import io
                import inspect
                import sphinxter
                import test.example

                parsed = sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'stat'), method=True)
                # {
                #     "name": "stat",
                #     "kind": "staticmethod",
                #     "description": "Some static stat",
                #     "signature": "(a, b, *args, **kwargs) -> list",
                #     "parameters": [
                #         {
                #             "name": "a",
                #             "description": "The a More stuff"
                #         },
                #         {
                #             "name": "b",
                #             "description": "The b",
                #             "more": "stuff"
                #         },
                #         {
                #             "name": "args"
                #         },
                #         {
                #             "name": "kwargs",
                #             "a": 1,
                #             "b": 2
                #         }
                #     ],
                #     "return": {
                #         "description": "things",
                #         "type": "list"
                #     }
                # }

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.method(parsed, indent=1)
                handle.getvalue()
                #
                #     .. staticmethod:: stat(a, b, *args, **kwargs) -> list
                #
                #         Some static stat
                #
                #         :param a: The a More stuff
                #         :param b: The b
                #         :param args:
                #         :param kwargs:
                #         :return: things
                #         :rtype: list
                #

            For a class method::

                parsed = sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'classy'), method=True)
                # {
                #     "name": "classy",
                #     "kind": "classmethod",
                #     "description": "Some class meth",
                #     "signature": "(a, b, *args, **kwargs)",
                #     "parameters": [
                #         {
                #             "name": "a",
                #             "description": "The a More stuff"
                #         },
                #         {
                #             "name": "b",
                #             "description": "The b",
                #             "more": "stuff"
                #         },
                #         {
                #             "name": "args"
                #         },
                #         {
                #             "name": "kwargs",
                #             "a": 1,
                #             "b": 2
                #         }
                #     ],
                #     "return": {
                #         "description": "things",
                #         "type": 'str'
                #     }
                # }

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.method(parsed, indent=1)
                handle.getvalue()
                #
                #     .. classmethod:: classy(a, b, *args, **kwargs)
                #
                #         Some class meth
                #
                #         :param a: The a More stuff
                #         :param b: The b
                #         :param args:
                #         :param kwargs:
                #         :return: things
                #         :rtype: str
                #

            And for a regular ol' method::

                parsed = sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'meth'), method=True)
                # {
                #     "name": "meth",
                #     "kind": "method",
                #     "description": "Some basic meth",
                #     "signature": "(a, b, *args, **kwargs)",
                #     "parameters": [
                #         {
                #             "name": "a",
                #             "description": "The a More stuff"
                #         },
                #         {
                #             "name": "b",
                #             "description": "The b",
                #             "more": "stuff"
                #         },
                #         {
                #             "name": "args"
                #         },
                #         {
                #             "name": "kwargs",
                #             "a": 1,
                #             "b": 2
                #         }
                #     ],
                #     "return": {
                #         "description": "things",
                #         "type": [
                #             'str',
                #             'None'
                #         ]
                #     },
                #     "raises": {
                #         "Exception": "if oh noes"
                #     },
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                # }

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.method(parsed, indent=1)
                handle.getvalue()
                #
                #     .. method:: meth(a, b, *args, **kwargs)
                #
                #         Some basic meth
                #
                #         :param a: The a More stuff
                #         :param b: The b
                #         :param args:
                #         :param kwargs:
                #         :return: things
                #         :rtype: str or None
                #         :raises Exception: if oh noes
                #
                #         **Usage**
                #
                #         Do some cool stuff::
                #
                #             like this
                #
                #         It's great
                #
        """

        self.line()
        self.line(f".. {parsed['kind']}:: {parsed['name']}{parsed['signature']}", indent)

        self.description(parsed, indent+1)
        self.routine(parsed, indent+1)
        self.usage(parsed, indent+1)

    def definition(self,
        parsed:dict,    # parsed documentation possibly keyed by definition
        indent:int      # amount to indent by
    ):
        """
        description: Writes a definition block if present, for describing how to define a class, ie models
        usage: |
            If there's definition, write with a header and proper blank lines::

                import io
                import yaml
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                class Example():
                    \"""
                    definition: |
                        Try this::

                            class Example:
                                pass
                    \"""

                parsed = yaml.safe_load(Example.__doc__)
                # {
                #     "definition": "Try this::\\n\\n    class Example:\\n        pass\\n"
                # }

                writer.definition(parsed, 1)
                handle.getvalue()
                #
                #     **Definition**
                #
                #     Try this::
                #
                #         class Example:
                #             pass
                #

            If there's nothing, do nothing::

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                parsed = {}

                writer.definition(parsed, 1)
                handle.getvalue()
                #
        """

        if "definition" not in parsed:
            return

        self.line("**Definition**", indent, before=True, after=True)
        self.lines(parsed["definition"].rstrip(), indent)

    def cls(self,
        parsed:dict,    # entire parsed documentation for a class
        indent:int=0    # amount to indent by
    ):
        """
        description: Writes class content as from :any:`Reader.cls`
        usage: |
            Given this class is part of the test.example module::

                class Complex:
                    \"""
                    description: Complex class
                    definition: |
                        make sure you do this::

                            wowsa

                        Ya sweet
                    \"""

                    a = None # The a team
                    b = None # The b team
                    \"""
                    Not as good as the a team
                    \"""
                    big = \"""
                    Stuff
                    \""" # Bunch a
                    \"""
                    a: 1
                    b: 2
                    \"""

                    def __init__(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: call me
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    @staticmethod
                    def stat(
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    )->list:
                        \"""
                        description: Some static stat
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return: things
                        \"""

                    @classmethod
                    def classy(
                        cls,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some class meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type: str
                        \"""

                    def meth(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some basic meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type:
                            - str
                            - None
                        raises:
                            Exception: if oh noes
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    class Subber:
                        \"""
                        Sub class
                        \"""
                        pass

                    class Excepter(Exception):
                        \"""
                        Sub exception
                        \"""
                        pass

            The documentation can be generated as such::

                import io
                import sphinxter
                import test.example

                parsed = sphinxter.Reader.cls(test.example.Complex)
                # {
                #     "attributes": [
                #         {
                #             "description": "The a team",
                #             "name": "a"
                #         },
                #         {
                #             "description": "The b team\\n\\nNot as good as the a team",
                #             "name": "b"
                #         },
                #         {
                #             "a": 1,
                #             "b": 2,
                #             "description": "Bunch a",
                #             "name": "big"
                #         }
                #     ],
                #     "classes": [
                #         {
                #             "attributes": [],
                #             "classes": [],
                #             "description": "Sub class",
                #             "exceptions": [],
                #             "kind": "class",
                #             "methods": [],
                #             "name": "Subber"
                #         }
                #     ],
                #     "definition": "make sure you do this::\\n\\n    wowsa\\n\\nYa sweet\\n",
                #     "description": "Complex class\\n\\ncall me",
                #     "exceptions": [
                #         {
                #             "attributes": [],
                #             "classes": [],
                #             "description": "Sub exception",
                #             "exceptions": [],
                #             "kind": "exception",
                #             "methods": [],
                #             "name": "Excepter"
                #         }
                #     ],
                #     "kind": "class",
                #     "methods": [
                #         {
                #             "description": "Some class meth",
                #             "kind": "classmethod",
                #             "name": "classy",
                #             "parameters": [
                #                 {
                #                     "description": "The a More stuff",
                #                     "name": "a"
                #                 },
                #                 {
                #                     "description": "The b",
                #                     "more": "stuff",
                #                     "name": "b"
                #                 },
                #                 {
                #                     "name": "args"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "name": "kwargs"
                #                 }
                #             ],
                #             "return": {
                #                 "description": "things",
                #                 "type": "str"
                #             },
                #             "signature": "(a, b, *args, **kwargs)"
                #         },
                #         {
                #             "description": "Some basic meth",
                #             "kind": "method",
                #             "name": "meth",
                #             "parameters": [
                #                 {
                #                     "description": "The a More stuff",
                #                     "name": "a"
                #                 },
                #                 {
                #                     "description": "The b",
                #                     "more": "stuff",
                #                     "name": "b"
                #                 },
                #                 {
                #                     "name": "args"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "name": "kwargs"
                #                 }
                #             ],
                #             "raises": {
                #                 "Exception": "if oh noes"
                #             },
                #             "return": {
                #                 "description": "things",
                #                 "type": [
                #                     "str",
                #                     "None"
                #                 ]
                #             },
                #             "signature": "(a, b, *args, **kwargs)",
                #             "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                #         },
                #         {
                #             "description": "Some static stat",
                #             "kind": "staticmethod",
                #             "name": "stat",
                #             "parameters": [
                #                 {
                #                     "description": "The a More stuff",
                #                     "name": "a"
                #                 },
                #                 {
                #                     "description": "The b",
                #                     "more": "stuff",
                #                     "name": "b"
                #                 },
                #                 {
                #                     "name": "args"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "name": "kwargs"
                #                 }
                #             ],
                #             "return": {
                #                 "description": "things",
                #                 "type": "list"
                #             },
                #             "signature": "(a, b, *args, **kwargs) -> list"
                #         }
                #     ],
                #     "name": "Complex",
                #     "parameters": [
                #         {
                #             "description": "The a More stuff",
                #             "name": "a"
                #         },
                #         {
                #             "description": "The b",
                #             "more": "stuff",
                #             "name": "b"
                #         },
                #         {
                #             "name": "args"
                #         },
                #         {
                #             "a": 1,
                #             "b": 2,
                #             "name": "kwargs"
                #         }
                #     ],
                #     "signature": "(a, b, *args, **kwargs)",
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                # }

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.cls(parsed, indent=1)
                handle.getvalue()
                #
                #     .. class:: Complex(a, b, *args, **kwargs)
                #
                #         Complex class
                #
                #         call me
                #
                #         **Definition**
                #
                #         make sure you do this::
                #
                #             wowsa
                #
                #         Ya sweet
                #
                #         :param a: The a More stuff
                #         :param b: The b
                #         :param args:
                #         :param kwargs:
                #
                #         **Usage**
                #
                #         Do some cool stuff::
                #
                #             like this
                #
                #         It's great
                #
                #         .. attribute:: a
                #
                #             The a team
                #
                #         .. attribute:: b
                #
                #             The b team
                #
                #             Not as good as the a team
                #
                #         .. attribute:: big
                #
                #             Bunch a
                #
                #         .. classmethod:: classy(a, b, *args, **kwargs)
                #
                #             Some class meth
                #
                #             :param a: The a More stuff
                #             :param b: The b
                #             :param args:
                #             :param kwargs:
                #             :return: things
                #             :rtype: str
                #
                #         .. method:: meth(a, b, *args, **kwargs)
                #
                #             Some basic meth
                #
                #             :param a: The a More stuff
                #             :param b: The b
                #             :param args:
                #             :param kwargs:
                #             :return: things
                #             :rtype: str or None
                #             :raises Exception: if oh noes
                #
                #             **Usage**
                #
                #             Do some cool stuff::
                #
                #                 like this
                #
                #             It's great
                #
                #         .. staticmethod:: stat(a, b, *args, **kwargs) -> list
                #
                #             Some static stat
                #
                #             :param a: The a More stuff
                #             :param b: The b
                #             :param args:
                #             :param kwargs:
                #             :return: things
                #             :rtype: list
                #
                #         .. class:: Subber
                #
                #             Sub class
                #
                #         .. exception:: Excepter
                #
                #             Sub exception
                #

            Say the test.exmaple module has this Exception::

                class Basic(Exception):
                    \"""
                    Basic Exception
                    \"""

            It's documentation is generated the same as any class::

                parsed = sphinxter.Reader.cls(test.example.Basic)
                # {
                #     "attributes": [],
                #     "classes": [],
                #     "description": "Basic Exception",
                #     "exceptions": [],
                #     "kind": "exception",
                #     "methods": [],
                #     "name": "Basic"
                # }

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.cls(parsed, indent=1)
                handle.getvalue()
                #
                #     .. exception:: Basic
                #
                #         Basic Exception
                #
        """

        self.line(f".. {parsed['kind']}:: {parsed['name']}{parsed.get('signature', '')}", indent, before=True)

        self.description(parsed, indent+1)
        self.definition(parsed, indent+1)
        self.routine(parsed, indent+1)
        self.usage(parsed, indent+1)
        self.attributes(parsed, indent+1)

        for method in parsed["methods"]:
            self.method(method, indent+1)

        for cls in parsed["classes"]:
            self.cls(cls, indent+1)

        for cls in parsed["exceptions"]:
            self.cls(cls, indent+1)

    def module(self,
        parsed:dict,    # entire parsed documentation for a class
        indent:int=0    # amount to indent by
    ):
        """
        description: |
            Writes module content as from :any:`Reader.module` but with a slight difference.

            Reading a module reads all the classes and functions for that module. Writing a module
            only writes documentation for that module because classes and functions don't have to
            be part of the same document as their parent module.
        usage: |
            Say the following is the example module::

                \"""
                description: mod me
                usage: |
                    Do some cool stuff::

                        like this

                    It's great
                \"""

                a = None # The a team
                b = None # The b team
                \"""
                Not as good as the a team
                \"""
                big = \"""
                Stuff
                \""" # Bunch a
                \"""
                a: 1
                b: 2
                \"""

                def func(
                    a:int,   # The a
                    b:'str', # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    \"""
                    description: Some basic func
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return:
                        description: things
                        type:
                        - str
                        - None
                    raises:
                        Exception: if oh noes
                    usage: |
                        Do some cool stuff::

                            like this

                        It's great
                    \"""


                class Basic(Exception):
                    \"""
                    Basic Exception
                    \"""


                class Complex:
                    \"""
                    description: Complex class
                    definition: |
                        make sure you do this::

                            wowsa

                        Ya sweet
                    \"""

                    a = None # The a team
                    b = None # The b team
                    \"""
                    Not as good as the a team
                    \"""
                    big = \"""
                    Stuff
                    \""" # Bunch a
                    \"""
                    a: 1
                    b: 2
                    \"""

                    def __init__(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: call me
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    @staticmethod
                    def stat(
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    )->list:
                        \"""
                        description: Some static stat
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return: things
                        \"""

                    @classmethod
                    def classy(
                        cls,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some class meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type: str
                        \"""

                    def meth(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some basic meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type:
                            - str
                            - None
                        raises:
                            Exception: if oh noes
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    class Subber:
                        \"""
                        Sub class
                        \"""
                        pass

                    class Excepter(Exception):
                        \"""
                        Sub exception
                        \"""
                        pass


            The documentation can be generated as such::

                import io
                import sphinxter
                import test.example

                parsed = sphinxter.Reader.module(test.example)
                # {
                #     "attributes": [
                #         {
                #             "description": "The a team",
                #             "name": "a"
                #         },
                #         {
                #             "description": "The b team\\n\\nNot as good as the a team",
                #             "name": "b"
                #         },
                #         {
                #             "a": 1,
                #             "b": 2,
                #             "description": "Bunch a",
                #             "name": "big"
                #         }
                #     ],
                #     "classes": [
                #         {
                #             "attributes": [
                #                 {
                #                     "description": "The a team",
                #                     "name": "a"
                #                 },
                #                 {
                #                     "description": "The b team\\n\\nNot as good as the a team",
                #                     "name": "b"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "description": "Bunch a",
                #                     "name": "big"
                #                 }
                #             ],
                #             "classes": [
                #                 {
                #                     "attributes": [],
                #                     "classes": [],
                #                     "description": "Sub class",
                #                     "exceptions": [],
                #                     "kind": "class",
                #                     "methods": [],
                #                     "name": "Subber"
                #                 }
                #             ],
                #             "definition": "make sure you do this::\\n\\n    wowsa\\n\\nYa sweet\\n",
                #             "description": "Complex class\\n\\ncall me",
                #             "exceptions": [
                #                 {
                #                     "attributes": [],
                #                     "classes": [],
                #                     "description": "Sub exception",
                #                     "exceptions": [],
                #                     "kind": "exception",
                #                     "methods": [],
                #                     "name": "Excepter"
                #                 }
                #             ],
                #             "kind": "class",
                #             "methods": [
                #                 {
                #                     "description": "Some class meth",
                #                     "kind": "classmethod",
                #                     "name": "classy",
                #                     "parameters": [
                #                         {
                #                             "description": "The a More stuff",
                #                             "name": "a"
                #                         },
                #                         {
                #                             "description": "The b",
                #                             "more": "stuff",
                #                             "name": "b"
                #                         },
                #                         {
                #                             "name": "args"
                #                         },
                #                         {
                #                             "a": 1,
                #                             "b": 2,
                #                             "name": "kwargs"
                #                         }
                #                     ],
                #                     "return": {
                #                         "description": "things",
                #                         "type": "str"
                #                     },
                #                     "signature": "(a, b, *args, **kwargs)"
                #                 },
                #                 {
                #                     "description": "Some basic meth",
                #                     "kind": "method",
                #                     "name": "meth",
                #                     "parameters": [
                #                         {
                #                             "description": "The a More stuff",
                #                             "name": "a"
                #                         },
                #                         {
                #                             "description": "The b",
                #                             "more": "stuff",
                #                             "name": "b"
                #                         },
                #                         {
                #                             "name": "args"
                #                         },
                #                         {
                #                             "a": 1,
                #                             "b": 2,
                #                             "name": "kwargs"
                #                         }
                #                     ],
                #                     "raises": {
                #                         "Exception": "if oh noes"
                #                     },
                #                     "return": {
                #                         "description": "things",
                #                         "type": [
                #                             "str",
                #                             "None"
                #                         ]
                #                     },
                #                     "signature": "(a, b, *args, **kwargs)",
                #                     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                #                 },
                #                 {
                #                     "description": "Some static stat",
                #                     "kind": "staticmethod",
                #                     "name": "stat",
                #                     "parameters": [
                #                         {
                #                             "description": "The a More stuff",
                #                             "name": "a"
                #                         },
                #                         {
                #                             "description": "The b",
                #                             "more": "stuff",
                #                             "name": "b"
                #                         },
                #                         {
                #                             "name": "args"
                #                         },
                #                         {
                #                             "a": 1,
                #                             "b": 2,
                #                             "name": "kwargs"
                #                         }
                #                     ],
                #                     "return": {
                #                         "description": "things",
                #                         "type": "list"
                #                     },
                #                     "signature": "(a, b, *args, **kwargs) -> list"
                #                 }
                #             ],
                #             "name": "Complex",
                #             "parameters": [
                #                 {
                #                     "description": "The a More stuff",
                #                     "name": "a"
                #                 },
                #                 {
                #                     "description": "The b",
                #                     "more": "stuff",
                #                     "name": "b"
                #                 },
                #                 {
                #                     "name": "args"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "name": "kwargs"
                #                 }
                #             ],
                #             "signature": "(a, b, *args, **kwargs)",
                #             "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                #         }
                #     ],
                #     "description": "mod me",
                #     "exceptions": [
                #         {
                #             "attributes": [],
                #             "classes": [],
                #             "description": "Basic Exception",
                #             "exceptions": [],
                #             "kind": "exception",
                #             "methods": [],
                #             "name": "Basic"
                #         }
                #     ],
                #     "functions": [
                #         {
                #             "description": "Some basic func",
                #             "kind": "function",
                #             "name": "func",
                #             "parameters": [
                #                 {
                #                     "description": "The a More stuff",
                #                     "name": "a",
                #                     "type": "int"
                #                 },
                #                 {
                #                     "description": "The b",
                #                     "more": "stuff",
                #                     "name": "b",
                #                     "type": "str"
                #                 },
                #                 {
                #                     "name": "args"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "name": "kwargs"
                #                 }
                #             ],
                #             "raises": {
                #                 "Exception": "if oh noes"
                #             },
                #             "return": {
                #                 "description": "things",
                #                 "type": [
                #                     "str",
                #                     "None"
                #                 ]
                #             },
                #             "signature": "(a: int, b: 'str', *args, **kwargs)",
                #             "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                #         }
                #     ],
                #     "name": "test.example",
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                # }

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.module(parsed, indent=1)
                handle.getvalue()
                #
                #     .. module:: test.example
                #
                #     mod me
                #
                #     **Usage**
                #
                #     Do some cool stuff::
                #
                #         like this
                #
                #     It's great
                #
                #     .. attribute:: a
                #
                #         The a team
                #
                #     .. attribute:: b
                #
                #         The b team
                #
                #         Not as good as the a team
                #
                #     .. attribute:: big
                #
                #         Bunch a
                #

            Notice how no functions or classes are written.
        """

        self.line(f".. module:: {parsed['name']}", indent, before=True)

        self.description(parsed, indent)
        self.usage(parsed, indent)
        self.attributes(parsed, indent)

    def toctree(self,
        paths:'list[str]',  # paths for the toc
        indent:int=0        # amount to indent by
    ):
        """
        description: Writes a toctree to the index document, hiding it so it'll appear to the left.
        usage: |
            Generating a toctree::

                import io
                import sphinxter

                document = sphinxter.Document(None, "test.example", None, '    ')
                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.toctree(['self', '*'], indent=1)
                handle.getvalue()
                #
                #     .. toctree::
                #         :maxdepth: 1
                #         :glob:
                #         :hidden:
                #
                #         self
                #         *
                #
        """
        self.line(".. toctree::", indent, before=True)
        self.line(":maxdepth: 1", indent+1)
        self.line(":glob:", indent+1)
        self.line(":hidden:", indent+1, after=True)

        for path in paths:
            self.line(path, indent+1)

    def dump(self):
        """
        description: Writes out an entire document
        usage: |
            Give the entire test.example module::

                \"""
                description: mod me
                usage: |
                    Do some cool stuff::

                        like this

                    It's great
                \"""

                a = None # The a team
                b = None # The b team
                \"""
                Not as good as the a team
                \"""
                big = \"""
                Stuff
                \""" # Bunch a
                \"""
                a: 1
                b: 2
                \"""

                def func(
                    a:int,   # The a
                    b:'str', # The b
                    *args,   #
                    **kwargs # a: 1
                            # b: 2
                ):
                    \"""
                    description: Some basic func
                    parameters:
                    a: More stuff
                    b:
                        more: stuff
                    return:
                        description: things
                        type:
                        - str
                        - None
                    raises:
                        Exception: if oh noes
                    usage: |
                        Do some cool stuff::

                            like this

                        It's great
                    \"""


                class Basic(Exception):
                    \"""
                    Basic Exception
                    \"""


                class Complex:
                    \"""
                    description: Complex class
                    definition: |
                        make sure you do this::

                            wowsa

                        Ya sweet
                    \"""

                    a = None # The a team
                    b = None # The b team
                    \"""
                    Not as good as the a team
                    \"""
                    big = \"""
                    Stuff
                    \""" # Bunch a
                    \"""
                    a: 1
                    b: 2
                    \"""

                    def __init__(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: call me
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    @staticmethod
                    def stat(
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    )->list:
                        \"""
                        description: Some static stat
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return: things
                        \"""

                    @classmethod
                    def classy(
                        cls,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some class meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type: str
                        \"""

                    def meth(
                        self,
                        a,       # The a
                        b,       # The b
                        *args,   #
                        **kwargs # a: 1
                                # b: 2
                    ):
                        \"""
                        description: Some basic meth
                        parameters:
                        a: More stuff
                        b:
                            more: stuff
                        return:
                            description: things
                            type:
                            - str
                            - None
                        raises:
                            Exception: if oh noes
                        usage: |
                            Do some cool stuff::

                                like this

                            It's great
                        \"""

                    class Subber:
                        \"""
                        Sub class
                        \"""
                        pass

                    class Excepter(Exception):
                        \"""
                        Sub exception
                        \"""
                        pass

            Generatig the whole shebang::

                import io
                import sphinxter
                import test.example

                parsed = sphinxter.Reader.module(test.example)
                # {
                #     "attributes": [
                #         {
                #             "description": "The a team",
                #             "name": "a"
                #         },
                #         {
                #             "description": "The b team\\n\\nNot as good as the a team",
                #             "name": "b"
                #         },
                #         {
                #             "a": 1,
                #             "b": 2,
                #             "description": "Bunch a",
                #             "name": "big"
                #         }
                #     ],
                #     "classes": [
                #         {
                #             "attributes": [
                #                 {
                #                     "description": "The a team",
                #                     "name": "a"
                #                 },
                #                 {
                #                     "description": "The b team\\n\\nNot as good as the a team",
                #                     "name": "b"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "description": "Bunch a",
                #                     "name": "big"
                #                 }
                #             ],
                #             "classes": [
                #                 {
                #                     "attributes": [],
                #                     "classes": [],
                #                     "description": "Sub class",
                #                     "exceptions": [],
                #                     "kind": "class",
                #                     "methods": [],
                #                     "name": "Subber"
                #                 }
                #             ],
                #             "definition": "make sure you do this::\\n\\n    wowsa\\n\\nYa sweet\\n",
                #             "description": "Complex class\\n\\ncall me",
                #             "exceptions": [
                #                 {
                #                     "attributes": [],
                #                     "classes": [],
                #                     "description": "Sub exception",
                #                     "exceptions": [],
                #                     "kind": "exception",
                #                     "methods": [],
                #                     "name": "Excepter"
                #                 }
                #             ],
                #             "kind": "class",
                #             "methods": [
                #                 {
                #                     "description": "Some class meth",
                #                     "kind": "classmethod",
                #                     "name": "classy",
                #                     "parameters": [
                #                         {
                #                             "description": "The a More stuff",
                #                             "name": "a"
                #                         },
                #                         {
                #                             "description": "The b",
                #                             "more": "stuff",
                #                             "name": "b"
                #                         },
                #                         {
                #                             "name": "args"
                #                         },
                #                         {
                #                             "a": 1,
                #                             "b": 2,
                #                             "name": "kwargs"
                #                         }
                #                     ],
                #                     "return": {
                #                         "description": "things",
                #                         "type": "str"
                #                     },
                #                     "signature": "(a, b, *args, **kwargs)"
                #                 },
                #                 {
                #                     "description": "Some basic meth",
                #                     "kind": "method",
                #                     "name": "meth",
                #                     "parameters": [
                #                         {
                #                             "description": "The a More stuff",
                #                             "name": "a"
                #                         },
                #                         {
                #                             "description": "The b",
                #                             "more": "stuff",
                #                             "name": "b"
                #                         },
                #                         {
                #                             "name": "args"
                #                         },
                #                         {
                #                             "a": 1,
                #                             "b": 2,
                #                             "name": "kwargs"
                #                         }
                #                     ],
                #                     "raises": {
                #                         "Exception": "if oh noes"
                #                     },
                #                     "return": {
                #                         "description": "things",
                #                         "type": [
                #                             "str",
                #                             "None"
                #                         ]
                #                     },
                #                     "signature": "(a, b, *args, **kwargs)",
                #                     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                #                 },
                #                 {
                #                     "description": "Some static stat",
                #                     "kind": "staticmethod",
                #                     "name": "stat",
                #                     "parameters": [
                #                         {
                #                             "description": "The a More stuff",
                #                             "name": "a"
                #                         },
                #                         {
                #                             "description": "The b",
                #                             "more": "stuff",
                #                             "name": "b"
                #                         },
                #                         {
                #                             "name": "args"
                #                         },
                #                         {
                #                             "a": 1,
                #                             "b": 2,
                #                             "name": "kwargs"
                #                         }
                #                     ],
                #                     "return": {
                #                         "description": "things",
                #                         "type": "list"
                #                     },
                #                     "signature": "(a, b, *args, **kwargs) -> list"
                #                 }
                #             ],
                #             "name": "Complex",
                #             "parameters": [
                #                 {
                #                     "description": "The a More stuff",
                #                     "name": "a"
                #                 },
                #                 {
                #                     "description": "The b",
                #                     "more": "stuff",
                #                     "name": "b"
                #                 },
                #                 {
                #                     "name": "args"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "name": "kwargs"
                #                 }
                #             ],
                #             "signature": "(a, b, *args, **kwargs)",
                #             "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                #         }
                #     ],
                #     "description": "mod me",
                #     "exceptions": [
                #         {
                #             "attributes": [],
                #             "classes": [],
                #             "description": "Basic Exception",
                #             "exceptions": [],
                #             "kind": "exception",
                #             "methods": [],
                #             "name": "Basic"
                #         }
                #     ],
                #     "functions": [
                #         {
                #             "description": "Some basic func",
                #             "kind": "function",
                #             "name": "func",
                #             "parameters": [
                #                 {
                #                     "description": "The a More stuff",
                #                     "name": "a",
                #                     "type": "int"
                #                 },
                #                 {
                #                     "description": "The b",
                #                     "more": "stuff",
                #                     "name": "b",
                #                     "type": "str"
                #                 },
                #                 {
                #                     "name": "args"
                #                 },
                #                 {
                #                     "a": 1,
                #                     "b": 2,
                #                     "name": "kwargs"
                #                 }
                #             ],
                #             "raises": {
                #                 "Exception": "if oh noes"
                #             },
                #             "return": {
                #                 "description": "things",
                #                 "type": [
                #                     "str",
                #                     "None"
                #                 ]
                #             },
                #             "signature": "(a: int, b: 'str', *args, **kwargs)",
                #             "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                #         }
                #     ],
                #     "name": "test.example",
                #     "usage": "Do some cool stuff::\\n\\n    like this\\n\\nIt's great\\n"
                # }

                document = sphinxter.Document(None, "test.example", ['self', '*'], '    ')

                for function in parsed["functions"]:
                    document.add("test.example", "function", function, 0)

                for cls in parsed["classes"]:
                    document.add("test.example", "class", cls, 0)

                handle = io.StringIO()

                writer = sphinxter.Writer(document, handle)

                writer.dump()
                handle.getvalue()
                # .. created by sphinxter
                # .. default-domain:: py
                #
                # test.example
                # ============
                #
                # .. toctree::
                #     :maxdepth: 1
                #     :glob:
                #     :hidden:
                #
                #     self
                #     *
                #
                # .. currentmodule:: test.example
                #
                # .. function:: func(a: int, b: 'str', *args, **kwargs)
                #
                #     Some basic func
                #
                #     :param a: The a More stuff
                #     :type a: int
                #     :param b: The b
                #     :type b: str
                #     :param args:
                #     :param kwargs:
                #     :return: things
                #     :rtype: str or None
                #     :raises Exception: if oh noes
                #
                #     **Usage**
                #
                #     Do some cool stuff::
                #
                #         like this
                #
                #     It's great
                #
                # .. class:: Complex(a, b, *args, **kwargs)
                #
                #     Complex class
                #
                #     call me
                #
                #     **Definition**
                #
                #     make sure you do this::
                #
                #         wowsa
                #
                #     Ya sweet
                #
                #     :param a: The a More stuff
                #     :param b: The b
                #     :param args:
                #     :param kwargs:
                #
                #     **Usage**
                #
                #     Do some cool stuff::
                #
                #         like this
                #
                #     It's great
                #
                #     .. attribute:: a
                #
                #         The a team
                #
                #     .. attribute:: b
                #
                #         The b team
                #
                #         Not as good as the a team
                #
                #     .. attribute:: big
                #
                #         Bunch a
                #
                #     .. classmethod:: classy(a, b, *args, **kwargs)
                #
                #         Some class meth
                #
                #         :param a: The a More stuff
                #         :param b: The b
                #         :param args:
                #         :param kwargs:
                #         :return: things
                #         :rtype: str
                #
                #     .. method:: meth(a, b, *args, **kwargs)
                #
                #         Some basic meth
                #
                #         :param a: The a More stuff
                #         :param b: The b
                #         :param args:
                #         :param kwargs:
                #         :return: things
                #         :rtype: str or None
                #         :raises Exception: if oh noes
                #
                #         **Usage**
                #
                #         Do some cool stuff::
                #
                #             like this
                #
                #         It's great
                #
                #     .. staticmethod:: stat(a, b, *args, **kwargs) -> list
                #
                #         Some static stat
                #
                #         :param a: The a More stuff
                #         :param b: The b
                #         :param args:
                #         :param kwargs:
                #         :return: things
                #         :rtype: list
                #
                #     .. class:: Subber
                #
                #         Sub class
                #
                #     .. exception:: Excepter
                #
                #         Sub exception
                #
        """

        self.line(".. created by sphinxter")
        self.line(".. default-domain:: py")

        self.line(self.document.title, before=True)
        self.line('=' * len(self.document.title))

        if self.document.toctree:
            self.toctree(self.document.toctree)

        module = None

        for index in sorted(self.document.contents.keys()):
            for content in self.document.contents[index]:

                if content.kind == "module":
                    self.module(content.parsed)
                    module = content.module
                elif module != content.module:
                    module = content.module
                    self.line(f".. currentmodule:: {module}", before=True)

                if content.kind == "function":
                    self.function(content.parsed)

                if content.kind in ["class", "exception"]:
                    self.cls(content.parsed)

"""
Module for reading documentation from resources
"""

# pylint: disable=too-many-branches, too-many-locals, too-few-public-methods

import io
import ast
import inspect
import token
import tokenize
import yaml

import logging

class Reader:
    """
    description: Static class for reading doc strings and comments into dict's
    document: reader
    """

    @staticmethod
    def source(
        resource # what to extract the source from
    ):
        """
        description: Reads the source, removing any overall indent
        parameters:
            resource:
                type:
                - module
                - function
                - class
                - method
        return:
            description: The non-indented source
            type: str
        usage: |
            Consider the sub class in a test.example module::

                class Complex:

                    class Subber:
                        \"""
                        Sub class
                        \"""

                        pass

            The source for Subber would be indented from inspect.getsource()
            which can't be parsed properly because of the initial indent::

                import inspect
                import test.example

                inspect.getsource(test.example.Complex.Subber)
                #     class Subber:
                #         \"""
                #         Sub class
                #         \"""
                #         pass
                #

            This prevents that problem::

                import sphinxter
                import test.example

                sphinxter.Reader.source(test.example.Complex.Subber)
                # class Subber:
                #     \"""
                #     Sub class
                #     \"""
                #     pass
                #
        """

        indent = None
        lines = []

        for line in inspect.getsourcelines(resource)[0]:

            if indent is None:
                indent = 0
                for letter in line:
                    if letter in [' ', "\t"]:
                        indent += 1
                    else:
                        break

            lines.append(line[indent:])

        return "".join(lines)

    @staticmethod
    def parse(
            docstring:str # the docstring (or string after an attribute)
        )->dict:
        """
        description: Parses a docstring into YAML, defaulting to description
        return:
            description: The parsed doctring
        usage: |
            If you just have a plain docstring, it'll return a dict
            with that docstring as the description::

                import sphinxter

                def plain():
                    \"""
                    A plain function
                    \"""

                sphinxter.Reader.parse(plain.__doc__)
                # {
                #     "description": "A plain function"
                # }

            If you have straight YAML it's return that as is::

                def exact():
                    \"""
                    description: An exact function
                    \"""

                sphinxter.Reader.parse(exact.__doc__)
                # {
                #     "description": "An exact function"
                # }

            If the string is blank, it'll return an empty dict::

                sphinxter.Reader.parse("")
                # {}
        """

        if docstring:
            parsed = yaml.safe_load(docstring)
            if isinstance(parsed, str):
                parsed = {"description": parsed}
        else:
            parsed = {}

        return parsed

    @classmethod
    def update(cls,
        primary:dict,   # The parsed dict to update
        secondary:dict, # The parsed dict to update with
        skip=None       # What dict keys to skip for updating
    ):
        """
        description: Updates an existing parsed dict with another, concatenating the descriptions
        parameters:
            skip:
                type:
                - None
                - str
                - list(str)
        usage: |
            This is used mainly to combine short and long descriptions::

                import sphinxter

                class Example:

                    attribute = None # This is an attribute
                    \"""
                    description: It's one of my favorites
                    type: str
                    \"""

                primary = {
                    "description": "This is an attribute"
                }

                secondary = {
                    "description": "It's one of my favorites",
                    "type": "str"
                }

                sphinxter.Reader.update(primary, secondary)
                primary
                # {
                #     "description": "This is an attribute\\n\\nIt's one of my favorites",
                #     "type": "str"
                # }

            It's also used to inject __init___ into a class, but not overwriting what matters::

                class Example:
                    \"""
                    An example class
                    \"""

                    def __init__(self,
                        foo:str # The foo arg
                    ):

                        return True

                primary = {
                    "name": "Example",
                    "description": "An example class"
                }

                secondary = {
                    "name": "Example.__init__",
                    "signature": "(foo: str)",
                    "parameters": [
                        {
                            "name": "foo",
                            "description": "The foo arg",
                            "type": "str"
                        }
                    ]
                }

                sphinxter.Reader.update(primary, secondary, "name")
                primary
                # {
                #     "name": "Example",
                #     "description": "An example class",
                #     "signature": "(foo: str)",
                #     "parameters": [
                #         {
                #             "name": "foo",
                #             "description": "The foo arg",
                #             "type": "str"
                #         }
                #     ]
                # }
        """

        if skip is None:
            skip = []

        if not isinstance(skip, list):
            skip = [skip]

        for name, value in secondary.items():

            if name in skip:
                continue

            if name == "description" and "description" in primary:
                primary[name] += "\n\n" + value
            else:
                primary[name] = value

    @classmethod
    def comments(cls,
        resource # what to read the parameter comments from
    )->dict:
        """
        description: Reads parameters comments from a function or method
        return: dict of parsed comments, keyed by parameter
        parameters:
            resource:
                type:
                - function
                - method
        usage: |
            You can put comments after parameters in a function or method and they
            can be parsed as YAML, just like a docstring.

            Say this code is in the test.example module::

                def func(
                    a:int,   # The a
                    b:'str', # The b
                    *args,   #
                    **kwargs # a: 1
                             # b: 2
                ):
                    pass

            You can extra the comments like so::

                import sphinxter
                import test.example

                sphinxter.Reader.comments(test.example.func)
                # {
                #     "a": {
                #         "description": "The a"
                #     },
                #     "args": {},
                #     "b": {
                #         "description": "The b"
                #     },
                #     "kwargs": {
                #         "a": 1,
                #         "b": 2
                #     }
                # }
        """

        parens = 0
        param = None
        params = False
        name = False
        comments = {}
        parseds = {}

        source = io.StringIO(cls.source(resource))

        for parsed in tokenize.generate_tokens(source.readline):
            if parsed.type == token.OP:
                if parsed.string == '(':
                    if parens == 0:
                        params = True
                        name = True
                    parens += 1
                elif parsed.string == ')':
                    parens -= 1
                    if parens == 0:
                        break
            elif parsed.type == token.NL:
                name = True
            elif parsed.type == token.NAME and name:
                if params:
                    param = parsed.string
                    parseds[param] = {}
                    name = False
            elif parsed.type == token.COMMENT:
                if param is not None:
                    comment = parsed.string[2:].rstrip()
                    if not comment:
                        continue
                    if param not in comments:
                        comments[param] = comment
                    else:
                        comments[param] = f"{comments[param]}\n{comment}"

        for param, comment in comments.items():
            logging.info("%s parameter: %s", resource.__name__, param)
            parseds[param].update(cls.parse(comment))

        return parseds

    @staticmethod
    def annotations(
        resource # what to extract annotations from
    )->dict:
        """
        description: Read annotations in a format better for updating
        parameters:
            resource:
                type:
                - function
                - method
        return: dict of annotations, with parameters and return keys
        usage: |
            You can use regular annotations and they can be extracted to
            update information about parameters and functions/methods
            themelves.

            Say this code is in the test.example module::

                def func(
                    a:int,   # The a
                    b:'str', # The b
                    *args,   #
                    **kwargs # a: 1
                             # b: 2
                ):
                    pass

            You can extra the annotations like so::

                import sphinxter
                import test.example

                sphinxter.Reader.annotations(test.example.func)
                # {
                #     "parameters": {
                #         "a": {
                #             "type": "int"
                #         },
                #         "b": {
                #             "type": "str"
                #         }
                #     },
                #     "return": {}
                # }
        """

        parseds = {
            "parameters": {},
            "return": {}
        }

        for name, annotation in inspect.get_annotations(resource).items():

            if not isinstance(annotation, str):
                annotation = annotation.__name__

            if name == "return":
                parseds["return"] = {"type": annotation}
            else:
                parseds["parameters"][name] = {"type": annotation}

        return parseds

    @classmethod
    def routine(cls,
        resource,            # what to read from
        method:bool=False    # whether this is a method
    )->dict:
        """
        description: |
            Reads all the documentation from a function or method for :any:`Writer.function` or :any:`Writer.method`

            Of special note is parameters. What's returned at the key of "parameters" is a list of dictionaries. But
            when specifiying parameter in the YAML, use a dict keyed by parameter name. The signature information
            is updated from the parameter comments and then from the dict in the YAML. If descriptions are specified
            in both areas, they'll be joined witha space, the signature comment going first.
        parameters:
            resource:
                type:
                - function
                - method
        return: dict of routine documentation
        usage: |
            .. note::

                This expects resources from inspect.getattr_static(), not getattr() and
                not directly off modules or classes or instances.

            Say this function is part of the test.example module::

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

            Reading all the documentation for a function is as easy as::

                import inspect
                import sphinxter
                import test.example

                sphinxter.Reader.routine(inspect.getattr_static(test.example, 'func'))
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

            Methods aren't much different, and include a method key, that's either '', 'class', or 'static'.

            Assume we're still in the test.example module and have this class::

                class Complex:

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

            Extract the documentation for each like so::

                import inspect
                import sphinxter
                import test.example

                sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'stat'), method=True)
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

                sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'classy'), method=True)
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

                sphinxter.Reader.routine(inspect.getattr_static(test.example.Complex, 'meth'), method=True)
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
        """

        logging.info("routine: %s", resource.__name__)

        if isinstance(resource, staticmethod):
            kind = "staticmethod"
            signature = inspect.signature(resource)
            annotations = cls.annotations(resource)
        elif isinstance(resource, classmethod):
            kind = "classmethod"
            signature = inspect.signature(resource.__func__)
            annotations = cls.annotations(resource.__func__)
        else:
            kind = "method"
            signature = inspect.signature(resource)
            annotations = cls.annotations(resource)

        if method and not isinstance(resource, (staticmethod)):
            signature = signature.replace(parameters=list(signature.parameters.values())[1:])

        parsed = {
            "name": resource.__name__,
            "signature": str(signature)
        }

        parsed["kind"] = kind if method else "function"

        lookup = {}
        comments = cls.comments(resource)

        for name in signature.parameters:

            parsed.setdefault("parameters", [])

            parameter = {
                "name": name
            }

            parameter.update(comments.get(name, {}))
            parameter.update(annotations["parameters"].get(name, {}))

            parsed["parameters"].append(parameter)
            lookup[name] = parameter

        for parsed_name, parsed_value in cls.parse(resource.__doc__).items():
            if parsed_name == "parameters":
                for parameter_name, parameter_value in parsed_value.items():
                    parameter_parsed = {"description": parameter_value} if isinstance(parameter_value, str) else parameter_value
                    for parameter_parsed_name, parameter_parsed_value in parameter_parsed.items():
                        if parameter_parsed_name == "description" and "description" in lookup[parameter_name]:
                            lookup[parameter_name]["description"] += " " + parameter_parsed_value
                        else:
                            lookup[parameter_name][parameter_parsed_name] = parameter_parsed_value
            else:
                parsed[parsed_name] = parsed_value

        if "return" in parsed:
            if isinstance(parsed["return"], str):
                parsed["return"] = {"description": parsed["return"]}

        if annotations["return"] and "type" not in parsed.get("return", {}):
            parsed.setdefault("return", {})
            parsed["return"].update(annotations["return"])

        return parsed

    @classmethod
    def attributes(cls,
        resource # what to extract attributes from
    )->dict:
        """
        description: Read attributes from a module or class, including their comments and docstrings
        parameters:
            resource:
                type:
                - function
                - method
        usage: |
            If you have attributes on a module, say the test.example module::

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

            You can extract/combime the descriptions and/or YAML like so::

                import sphinxter
                import test.example

                sphinxter.Reader.attributes(test.example)
                # {
                #     "a": {
                #         "description": "The a team"
                #     },
                #     "b": {
                #         "description": "The b team\\n\\nNot as good as the a team"
                #     },
                #     "big": {
                #         "a": 1,
                #         "b": 2,
                #         "description": "Bunch a"
                #     }
                # }

            This works the same for a class, say the Complex class in the test.example module::

                class Complex:

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

            Extracting is just as easy::

                import sphinxter
                import test.example

                sphinxter.Reader.attributes(test.example.Complex)
                # {
                #     "a": {
                #         "description": "The a team"
                #     },
                #     "b": {
                #         "description": "The b team\\n\\nNot as good as the a team"
                #     },
                #     "big": {
                #         "a": 1,
                #         "b": 2,
                #         "description": "Bunch a"
                #     }
                # }
        """

        parseds = {}
        targets = []

        nodes = ast.parse(cls.source(resource))

        if inspect.isclass(resource):
            nodes = nodes.body[0]

        for node in nodes.body:

            if targets and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):

                logging.info("attribute docstring: %s", '-'.join(targets))

                parsed = cls.parse(node.value.value)
                for target in targets:
                    cls.update(parseds[target], parsed)

            elif isinstance(node, ast.Assign):

                targets = [target.id for target in node.targets]

                for target in targets:
                    parseds.setdefault(target, {})

                source = io.StringIO(inspect.getsourcelines(resource)[0][node.end_lineno - 1][node.end_col_offset + 1:])

                for tokenized in tokenize.generate_tokens(source.readline):
                    if tokenized.type == token.COMMENT:
                        comment = tokenized.string[2:].rstrip()
                        logging.info("attribute comment: %s", '-'.join(targets))
                        parsed = cls.parse(comment)
                        for target in targets:
                            parseds[target] = parsed

            else:

                targets = []

        return parseds

    @classmethod
    def cls(cls,
        resource # what to extract documentation from
    )->dict:
        """
        description: Reads all the documentation from a class for :any:`Writer.cls`
        parameters:
            resource:
                type: class
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

            Reading all the documentation is as easy as::

                import sphinxter
                import test.example

                sphinxter.Reader.cls(test.example.Complex)
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

            Notfice that the __init__ method documentation has been super imposed over the class documentation.

            Say we're still inthe test.example module::

                class Basic(Exception):
                    \"""
                    Basic Exception
                    \"""

            If a class is exception, it'll capture that::

                import sphinxter
                import test.example

                sphinxter.Reader.cls(test.example.Basic)
                # {
                #     "attributes": [],
                #     "classes": [],
                #     "description": "Basic Exception",
                #     "exceptions": [],
                #     "kind": "exception",
                #     "methods": [],
                #     "name": "Basic"
                # }
        """

        logging.info("class: %s", resource.__name__)

        parsed = {
            "name": resource.__name__,
            "kind": "exception" if Exception in resource.__bases__ else "class",
            "attributes": [],
            "methods": [],
            "classes": [],
            "exceptions": []
        }

        parsed.update(cls.parse(resource.__doc__))

        if "__init__" in resource.__dict__:
            cls.update(parsed, cls.routine(resource.__init__, method=True), skip=["name", "kind"])

        attributes = cls.attributes(resource)

        for name, attr in {name: inspect.getattr_static(resource, name) for name in sorted(resource.__dict__.keys())}.items():

            if (inspect.isfunction(attr) or isinstance(attr, (staticmethod, classmethod))):

                if name != "__init__":
                    parsed["methods"].append(cls.routine(attr, method=True))

            elif inspect.isclass(attr):

                cls_parsed = cls.cls(attr)

                if cls_parsed["kind"] == "exception":
                    parsed["exceptions"].append(cls_parsed)
                else:
                    parsed["classes"].append(cls_parsed)

            elif name in resource.__dict__ and not name.startswith('__') and not name.endswith('__'):

                attribute = {
                    "name": name
                }

                cls.update(attribute, attributes[name])

                parsed["attributes"].append(attribute)

        return parsed

    @classmethod
    def module(cls,
        resource # what to extract documentation from
    )->dict:
        """
        description: Reads all the documentation from a module for :any:`Writer.module`
        parameters:
            resource:
                type: module
        usage: |
            Say the following is the test.example module::

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

            Reading all the documentation is as easy as::

                import sphinxter
                import test.example

                sphinxter.Reader.module(test.example)
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
        """

        logging.info("module: %s", resource.__name__)

        parsed = {
            "name": resource.__name__,
            "attributes": [],
            "functions": [],
            "classes": [],
            "exceptions": []
        }

        parsed.update(cls.parse(resource.__doc__))

        attributes = cls.attributes(resource)

        for name, attr in {name: inspect.getattr_static(resource, name) for name in dir(resource)}.items():

            if inspect.isfunction(attr):

                parsed["functions"].append(cls.routine(attr))

            elif inspect.isclass(attr):

                cls_parsed = cls.cls(attr)

                if cls_parsed["kind"] == "exception":
                    parsed["exceptions"].append(cls_parsed)
                else:
                    parsed["classes"].append(cls_parsed)

            elif name in attributes:

                attribute = {
                    "name": name
                }

                cls.update(attribute, attributes[name])

                parsed["attributes"].append(attribute)

        return parsed

"""
module for Documents and their Content
"""

# pylint: disable=too-few-public-methods

class Document:
    """
    description: Document (rst) to write out
    document: document
    """

    path = None     # where to store the document
    title = None    # title of the document
    indent = None   # string to use for indenting
    toctree = None  # list of documents for toctree or False if none
    contents = None # document contents
    """
    type: dict
    description: |
        If a resource's document block has an order (default zero) that
        order is used as the key in the contents dict, to a list of contents
        for that order. That way, if nothing is specified, everything is added
        alphabetically. However, if you want a more obscure resource to go last,
        you just need to set the order greater that zero. Two resources at the
        same order are displayed the order in which they were added.
    """

    def __init__(self,
        path:str,   # where to store the
        title:str,  # title of the document
        toctree,    # list of documents for toctree or False if none
        indent:str  # string to use for indenting
    ):
        """
        parameters:
            toctree:
                type:
                - bool
                - list
        """

        self.path = path
        self.title = title
        self.toctree = toctree
        self.indent = indent
        self.contents = {}

    def add(self,
        module:str,     # Name of module this content is for
        kind:str,       # Kind of resource
        parsed:dict,    # The parsed documentation
        order:int       # Where to place this content
    ):
        """
        Adds content to a document
        """

        self.contents.setdefault(order, [])
        self.contents[order].append(self.Content(module, kind, parsed))

    class Content:
        """
        Content for a Document
        """

        module = None   # Name of module this content is for
        kind = None     # Kind of resource
        parsed = None   # The parsed documentation

        def __init__(self,
            module:str, # Name of module this content is for
            kind:str,   # Kind of resource
            parsed:dict # The parsed documentation
        ):

            self.module = module
            self.kind = kind
            self.parsed = parsed

"""
# Doc Handlers

A DocHandler processes a single python file into a page for your documentation.
"""
import ast
import importlib.util
import sys
import docstring_parser

from rubberdoc.config_provider import RubberDocConfig


class DocstringCoverage:
    """An object supporting Docstring Coverage.

    Attributes:
        docstring_potential (int): the number of docstring locations searched
        docstrings_found (int): the number of docstrings found
    """
    def __init__(self):
        self.docstring_potential: int = 0
        self.docstrings_found: int = 0
    
    def report(self):
        if not self.docstring_potential:
            return 'N/A'
        return (f"{self.docstrings_found} / {self.docstring_potential} "
                f" ({int(100 * (self.docstrings_found / self.docstring_potential))}%)")


class BaseDocHandler:
    """BaseDocHandler contains core functionality for converting python files to markdown.  

    It contains `get_`ers, `wrap_`ers, and a `process_`er.  

    The `get_`ers are a set of conveniences to get information about a node.  

    The `wrap_`ers wrap each component of a node and are built to be overriden for customization.  

    The `process_`er (specifically, `process_node`) determines the order of processed components of a node.
    This may also be overriden if you desire a different sequence of information, or if you wish to add your own `wrap_`ers.
    """
    def __init__(self, file_path: str, config: RubberDocConfig):
        self.file_path = file_path
        self.config = config
        self.doc: list = list()
        self.code: list = list()
        self.coverage = DocstringCoverage()
    
    def process(self) -> str:
        """Processes a file to markdown.

        This is the main driver called from the generator.

        Returns:
            str: A document processed to markdown.
        """   
        with open(self.file_path, 'r') as o:
            if str(self.file_path).endswith('.md'):
                return o.read()
            self.source_code = o.read()
            tree = ast.parse(self.source_code)
            self.__module_docstring(tree)
            self.__walk_tree(tree)
        return ''.join(self.doc)
    
    def __module_docstring(self, tree):
        """Places the module-level docstring at the top of the document.

        Args:
            tree: The root of the Abstract Syntax Tree
        """
        module_docstring = ast.get_docstring(tree)
        self.coverage.docstring_potential += 1
        if module_docstring:
            self.doc.append(module_docstring + '  \n')
            self.coverage.docstrings_found += 1
    
    def __walk_tree(self, tree):
        """Walks the Abstract Syntax Tree and calls `process_node` for each function or class `node`.

        Args:
            tree: The root of the Abstract Syntax Tree
        """
        for node in tree.body:
            level = 1
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                self.process_node(level, node)
                if isinstance(node, ast.ClassDef):
                    level += 1
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            self.process_node(level, child, node)
    
    def process_node(self, level: int, node: ast.ClassDef | ast.FunctionDef, parent=None):
        """Processes a function or class `node` into markdown and appends to doc.  

        This function can be overriden to determine the order of parsed elements of the node. 

        Args:
            level (int): level for indentation purposes  
            node (ast.ClassDef | ast.FunctionDef): the current node to be processed 
            parent (ast.ClassDef, optional): the parent class if a function node. Defaults to None.
        """
        if parent:
            self.doc.append(self.wrap_func_cls_lbl(parent.name))
        
        # function or class name
        self.doc.append(self.wrap_func_cls_name(level, node))
        
        
        docstring = self.get_parsed_docstring(node)
        self.doc.append(self.wrap_parsed_docstring(docstring))
        
        if self.config.output['include_source_code']:
            source_code = self.get_node_code(node)
            self.doc.append(self.wrap_codeblock(source_code))
    
    def get_full_docstring(self, node: ast.ClassDef | ast.FunctionDef) -> str:
        """Returns the docstring of the class or function `node`.  
        
        If no docstring is found in the node, a default is returned. 
        This default can be set in the configuration file.  

        While attempting to get the docstring of the node, this function 
        will also contribute to capturing the docstring coverage in the code base.
        """
        docstring = ast.get_docstring(node)
        self.coverage.docstring_potential += 1
        if docstring:
            self.coverage.docstrings_found += 1
        return  docstring or self.config.output['no_docstring_default']

    def get_node_code(self, node: ast.ClassDef | ast.FunctionDef) -> str:
        """Returns the codeblock of the class or function `node`."""
        return ast.get_source_segment(self.source_code, node)
    
    def get_parsed_docstring(self, node: ast.ClassDef | ast.FunctionDef) -> docstring_parser.Docstring:
        """Parses a `node`'s docstring with `docstring_parser`.

        Args:
            node (ast.ClassDef | ast.FunctionDef): Node from the `ast` tree

        Returns:
            Docstring: a docstring object 
        """
        return docstring_parser.parse(self.get_full_docstring(node))
    
    def get_function_params(self, node: ast.FunctionDef) -> list[str]:
        """Returns a list of parameters for the function `node`.  

        I would like to have this show the parameter types, but couldn't figure
        out how to do so. If you figure it out - please let me know!        
        """
        return [f"{a.arg}" for a in node.args.args]
    
    def get_class_bases(self, node: ast.ClassDef) -> list[str]:
        return [b.id for b in node.bases]
    
    def get_node_return_type(self, node: ast.ClassDef | ast.FunctionDef) -> str:
        return node.returns.id if node.returns else ''
    
    def wrap_func_cls_lbl(self, parent_name: str) -> str:
        return parent_name + '  \n'
    
    def wrap_func_cls_name(self, level: int, node: ast.ClassDef | ast.FunctionDef) -> str:
        """Wraps the function or class `node`'s name.  

        Args:
            level (int): The indentation level.
            node (ast.ClassDef | ast.FunctionDef): The node for parsing.
        """
        # avoid markdown collisions with dunder methods
        node_name = node.name
        if node_name.startswith('_') and node_name.endswith('_'):
            node_name = f"\{node_name}"

        # if class inherits let it be known!
        inherits = ''
        if isinstance(node, ast.ClassDef):
            bases = self.get_class_bases(node)
            if bases:
                inherits = f" ({', '.join(bases)})"

        return (f"{'#' * (level + 1)} "
                f"{'__def__ ' if isinstance(node, ast.FunctionDef) else '__class__ '}"
                f"{node_name}{inherits}  \n")
    
    def wrap_docstring(self, docstring: str) -> str:
        """Wraps the provided docstring for markdown."""
        return docstring + "  \n"
    
    def wrap_codeblock(self, code: str) -> str:
        """Wraps the provided codeblock for markdown."""
        c = '```\n'
        c += code
        c += '\n```\n'
        return c
    
    def wrap_parsed_docstring(self, docstring: docstring_parser.Docstring) -> str:
        """Wraps the provided parsed docstring.
        
        The parsed docstring object is parsed by the `docstring_parser` library.
        The nice part about this object is that it allows the author of the docstring 
        to adhere to whichever docstring standard they prefer and additionally supply any markdown 
        in the description.

        Args:
            docstring: Docstring object from docstring_parser library
        
        Returns:
            str: A string of the prepared docstring ready for being appended to the markdown doc.
        """
        docstring_builder = str()
        if docstring.short_description:
            docstring_builder += docstring.short_description + '  \n\n'
        if docstring.long_description:
            docstring_builder += docstring.long_description + '  \n'
        if docstring.params:
            params = self.wrap_docstring_params(docstring.params)
            docstring_builder += params
        if docstring.returns:
            returns = self.wrap_docstring_returns(docstring.returns)
            docstring_builder += returns
        return docstring_builder
    
    def wrap_docstring_params(self, params: list[docstring_parser.DocstringParam]) -> str:
        params_builder = str()
        for param in params:
            if not params_builder:
                params_builder += f"\n**{param.args[0].title()}s:**  \n\n"
            ps = str("- ")
            if param.arg_name:
                ps += f"`{param.arg_name}` "
            if param.is_optional:
                ps += f"(optional) "
            if param.type_name and not param.description:
                ps += f"{param.type_name} "
            if param.type_name and param.description:
                ps += f"(_{param.type_name}_) "
            if param.description:
                ps += f"- {param.description} "
            # if param.default:
            #     ps += f"__default__: {param.default} "
            ps += '  \n\n'
            params_builder += ps
        return params_builder
    
    def wrap_docstring_returns(self, returns: docstring_parser.DocstringReturns) -> str:
        returns_builder = "\n**Returns:**  \n\n"
        if returns.type_name:
            returns_builder += f"(_{returns.type_name}_) "
        if returns.description:
            returns_builder += f"{returns.description}"
        returns_builder += "  \n\n"
        return returns_builder

    

class MaterialMKDocsHandler(BaseDocHandler):
    """A spin on the BaseDocHandler centered towards MKDocs 'Material' theme.  

    This can be used in commandline generation like so:  
    `rubberdoc generate --style material`  

    Note that this expects the following minimal additions to your `mkdocs.yml` file:  

    ```
    theme: material
    markdown_extensions:
    - pymdownx.highlight:
        anchor_linenums: true
    - pymdownx.inlinehilite
    - pymdownx.snippets
    - pymdownx.superfences
    - pymdownx.tabbed:
        alternate_style: true 
    ```
    """
    def __init__(self, file_path: str, config: RubberDocConfig):
        super().__init__(file_path=file_path, config=config)
    
    def process_node(self, level: int, node: ast.ClassDef | ast.FunctionDef, parent=None):
        if parent:
            self.doc.append(self.wrap_func_cls_lbl(parent.name))
        
        # function or class name
        self.doc.append(self.wrap_func_cls_name(level, node))
        
        docstring = self.wrap_parsed_docstring(
            self.get_parsed_docstring(node))
        self.doc.append(self.wrap_docstring(docstring))
        
        if self.config.output['include_source_code']:
            source_code = self.get_node_code(node)
            self.doc.append(self.wrap_codeblock(source_code))

        self.doc.append('\n---  \n')
            
    def wrap_func_cls_lbl(self, parent_name: str):
        return f"<label class='class-label'>{parent_name}</label>  \n"
    
    def wrap_docstring(self, docstring: str) -> str:
        """Wraps the provided docstring for markdown.  
        
        If you are using RubberDoc generation from a python script,
        you could subclass the DocHandler and augment this method to your
        preferred style.
        """
        d = '=== "Documentation"\n'
        d += '\n'.join(f"    {d}" for d in docstring.splitlines())
        d += "  \n\n"
        return d
    
    def wrap_codeblock(self, code: str) -> str:
        """Wraps the provided codeblock for markdown.  
        
        If you are using RubberDoc generation from a python script,
        you could subclass the DocHandler and augment this method to your
        preferred style.
        """
        c = '=== "Code"\n'
        c += '    ```py\n'
        c += '\n'.join(f"    {l}" for l in code.splitlines())
        c += '\n    ```  \n'
        c += "  \n\n"
        return c


def doc_handler_selection(config: RubberDocConfig, style: str) -> BaseDocHandler | None:
    """Determines the DocHandler to provide given a `RubberDocConfig` and `style`"""
    cust_fp = config.output['custom_doc_handler_filepath']
    cust_cls = config.output['custom_doc_handler_class_name']
    handler = None
    if cust_fp and cust_cls:
        spec = importlib.util.spec_from_file_location(cust_cls, cust_fp)
        foo = importlib.util.module_from_spec(spec)
        sys.modules[cust_cls] = foo
        spec.loader.exec_module(foo)
        handler = getattr(foo, cust_cls, None)
    elif style.lower() == 'material':
        handler = MaterialMKDocsHandler
    elif style.lower() == 'default':
        handler = BaseDocHandler
    return handler
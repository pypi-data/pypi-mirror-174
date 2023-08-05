from rubberdoc.doc_handler import BaseDocHandler
from rubberdoc.config_provider import RubberDocConfig
import ast

class CustomDocHandler(BaseDocHandler):
    """A custom spin on the BaseDocHandler centered towards MKDocs 'Material' theme.  

    This custom DocHandler is meant to provide an example of how you might override 
    the methods of BaseDocHandler to create your own DocHandler class. 
    See the tutorial section for more details on how to implement this custom class. 

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
        """Override the `process_node` method with our own implementation.  
        
        This will allow us to reorder how each node is displayed. A node is a class or function definition.
        """
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
        """Override the `wrap_func_cls_lbl` method with our own implementation."""
        return f"<label class='class-label'>{parent_name}</label>  \n"
    
    def wrap_docstring(self, docstring: str) -> str:
        """Override the `wrap_docstring` method with our own implementation."""
        d = '=== "Documentation"\n'
        d += '\n'.join(f"    {d}" for d in docstring.splitlines())
        d += "  \n\n"
        return d
    
    def wrap_codeblock(self, code: str) -> str:
        """Override the `wrap_codeblock` method with our own implementation."""
        c = '=== "Code"\n'
        c += '    ```py\n'
        c += '\n'.join(f"    {l}" for l in code.splitlines())
        c += '\n    ```  \n'
        c += "  \n\n"
        return c

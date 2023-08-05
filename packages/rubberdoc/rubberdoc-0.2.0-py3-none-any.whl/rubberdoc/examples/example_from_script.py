from rubberdoc.generator import RubberDoc 
from rubberdoc.config_provider import RubberDocConfig
from rubberdoc.doc_handler import BaseDocHandler

class MyDocHandler(BaseDocHandler):
    """Custom DocHandler"""
    def __init__(self, file_path: str, config: RubberDocConfig):
        super().__init__(file_path, config)
    
    def wrap_codeblock(self, code: str) -> str:
        """Override the `wrap_codeblock` method to return nothing"""
        return ""

    def wrap_docstring(self, docstring: str) -> str:
        return '**DOCSTRING**  \n' + docstring + '  \n'

default_config = RubberDocConfig(path_to_config=None)

rd = RubberDoc(
    config=default_config,
    doc_handler=MyDocHandler)

rd.generate(
    input_directory=r"../rubberdoc/rubberdoc", 
    output_directory=r"../rubberdoc/docs/docs/reference")

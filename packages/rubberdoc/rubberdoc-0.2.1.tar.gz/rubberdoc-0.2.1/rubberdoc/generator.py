"""
Generates the documentation by walking through the provided directory, 
determining if the file is to be processed (according to the configuration), 
passing the file to the provided DocHandler, 
and saving the returned contents to the output_directory.
"""
import os
from pathlib import Path
import re

from rubberdoc.config_provider import RubberDocConfig
from rubberdoc.doc_handler import BaseDocHandler


class RubberDoc:
    def __init__(self, config: RubberDocConfig, doc_handler: BaseDocHandler):
        self.config: RubberDocConfig = config
        self.doc_handler: BaseDocHandler = doc_handler

    def generate(self, input_directory: str, output_directory: str):
        """Generates documentation from the `input_directory` to the `output_directory`.

        Args:
            input_directory (str): the path to the package 
            output_directory (str): the path to the directory for the generated documents
        """
        self.__clean_mds(output_directory)
        for (dirpath, _, filenames) in os.walk(input_directory):          
            if '__pycache__' in str(dirpath):
                continue
            for filename in filenames:
                py_file = Path(dirpath, filename)
                if self.__wants_to_write(py_file):
                    write_path = (
                        Path(output_directory) 
                        / py_file.relative_to(input_directory).parent
                        / self.__rename_file(Path(filename).stem))
                    handler = self.doc_handler(
                        file_path=Path(dirpath) / filename,
                        config=self.config)
                    processed_doc = handler.process()
                    self.__callback(py_file, write_path, handler.coverage.report())
                    
                    self.save(
                        to=write_path, 
                        content=processed_doc)
    
    @staticmethod
    def __callback(py_file, write_path, coverage_report):
        print('File: ', py_file)
        print('Destination: ', write_path)
        init_file = str(py_file).endswith('__init__.py')
        print('Docstring Coverage: ', 'N/A' if init_file else coverage_report)
        print()

    def __clean_mds(self, out_dir: str):
        for (dirpath, _, filenames) in os.walk(out_dir):
            for file in filenames:
                if file.endswith('.md'):
                    os.remove(Path(dirpath, file))
            try:
                os.rmdir(dirpath)
            except: 
                pass
    
    def __wants_to_write(self, file_path: str) -> bool:
        """Checks config to determine if this file should be written. 

        Args:
            file_path (str): the path to the file in question

        Returns:
            bool: whether to write the file or not
        """
        write_it = False
        for inc in self.config.input['include']:
            if re.search(inc, str(file_path)):
                write_it = True 
        for exc in self.config.input['exclude']:
            if re.search(exc, str(file_path)):
                write_it = False
        return write_it

    def save(self, to: str, content: str):
        os.makedirs(to.parent, exist_ok=True)
        with open(to, 'w+') as o:
            o.write(content)

    def __rename_file(self, filename):
        rn = self.config.output['rename']
        fn = rn.get(filename, filename)
        return fn + '.md'

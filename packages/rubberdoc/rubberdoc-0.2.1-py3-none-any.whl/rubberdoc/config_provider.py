"""
# Config Provider

A simple configuration file handler for RubberDoc.  

Default configurations are inititally provided, then overwritten with any 
custom configurations provided by the user. The default configuration looks like this:  

`default_config.json`  
```
{
    "input": {
        "include": [
            "\\.py$",
            "\\.md$"
        ],
        "exclude": [
            
        ]
    },
    "output": {
        "custom_doc_handler_filepath": "",
        "custom_doc_handler_class_name": "",
        "no_docstring_default": "_No docstring_",
        "include_source_code": true,
        "rename": {
            "__init__": "index"
        }
    }
}
```
"""
import json
from pathlib import Path

class RubberDocConfig:
    def __init__(self, path_to_config: str or None = None):
        self.input = dict() 
        self.output = dict()
        self.__load_config(path_to_config)


    def __load_config(self, path_to_config: str or None):
        p_def_conf = Path(__file__).parent / 'default_config.json'
        with open(p_def_conf, 'r') as o:
            conf = json.loads(o.read())
        if path_to_config and path_to_config.endswith('.json'):
            with open(path_to_config, 'r') as o:
                personalized = json.loads(o.read())
                conf.update(personalized)
        self.__bucket(conf)
    
    def __bucket(self, conf):
        self.input = conf['input']
        self.output = conf['output']

"""
Commandline commands powered by the `typer` library.  

This module gives us the ability to run RubberDoc from the commandline. 
A few basic commands are available:  

`rubberdoc version`  
`rubberdoc hello`  
`rubberdoc generate`  

See each one for more details.
"""
import os
import typer

from rubberdoc import __version__
from rubberdoc.generator import RubberDoc
from rubberdoc.doc_handler import doc_handler_selection
from rubberdoc.config_provider import RubberDocConfig


app = typer.Typer()

@app.command()
def version():
    """ show current version """
    typer.echo(f"RubberDoc v{__version__}")

@app.command()
def hello():
    """ say hello """
    typer.secho("🦆 Quack!", fg='yellow')

@app.command()
def generate(from_dir: str or None = None, 
             to_dir: str or None = None, 
             config: str or None = None,
             style: str = 'default'):
    """Generates documentation from `from-dir` to `to-dir`

    Args:
        from_dir (str, optional): The directory of your python codebase. Defaults to current working directory.
        to_dir (str, optional): The directory to generate .md files to. Defaults to '../docs'.
        config (str, optional): The direct path to a .json configuration file. Defaults to None.
        style (str, optional): Style generated. Defaults to 'default'.
    """
    rd_config = RubberDocConfig(path_to_config=config)
    doc_handler_cls = doc_handler_selection(rd_config, style)
    if doc_handler_cls:
        typer.echo(f"\nUsing {doc_handler_cls.__name__} for generation.\n")
        rd = RubberDoc(config=rd_config, doc_handler=doc_handler_cls)
        rd.generate(
            input_directory=from_dir or os.curdir, 
            output_directory=to_dir or '../docs')
    else:
        typer.secho(f"Incorrect DocHandler class provided", fg='red')
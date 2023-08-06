"""
"""
import os
import sys
import importlib
import inspect
import json

import jinja2
import click

import pynchon
LOGGER = pynchon.get_logger(__name__)
from pynchon import (annotate, util)
from .common import *
from .groups import entry
from .groups import project,gen,gen_api,gen_cli,ast

@kommand(
    name='entrypoints', parent=project,
    formatters=dict(markdown=pynchon.T_ENTRYPOINTS),
    options=[ OPT_file_setupcfg, OPT_format,
        OPT_stdout, OPT_output, OPT_header])
def project_entrypoints(format, file, stdout, output, header):
    """
    Describe entrypoints for this project (parses setup.cfg)
    """
    return util.load_entrypoints(
            util.load_setupcfg(file=file))


@kommand(
    name='click', parent=gen_cli,
    formatters=dict(markdown=pynchon.T_TOC_CLI),
    options=[
        OPT_format, OPT_stdout,OPT_output,
        OPT_header, OPT_file, OPT_name, OPT_module,])
def click_dump(format, module, name, file, output, stdout, header):
    """
    Autogenenerate docs for python CLIs using click
    """
    result = []
    if name and not module:
        module, name = name.split(':')
    if (module and name):
        mod = importlib.import_module(module)
        entrypoint = getattr(mod, name)
    else:
        msg = "No entrypoint found"
        LOGGER.warning(msg)
        return dict(error=msg)
    LOGGER.debug(f"Recursive help for `{module}:{name}`")
    result = util.click_recursive_help(entrypoint, parent=None)
    package = module.split('.')[0]
    header = f"CLI entry-points for {package} \n\n{header}"
    return dict(commands=result, header=header)


def markdown(**result):
    return result['header'] + "\n".join(result['blocks'])
@kommand(name='toc', parent=gen_api,
    formatters=dict(markdown=markdown),
    options=[OPT_format_markdown, OPT_output,
        OPT_file, OPT_stdout, OPT_header, OPT_package])
def toc(package, file, output, format, stdout, header):
    """
    Generate table-of-contents
    """

    module = util.get_module(package=package, file=file)
    result = util.visit_module(module=module, module_name=package)
    return dict(
        header=f"## API for '{package}' package\n\n{header}\n\n" + '-' * 80,
        blocks=result)

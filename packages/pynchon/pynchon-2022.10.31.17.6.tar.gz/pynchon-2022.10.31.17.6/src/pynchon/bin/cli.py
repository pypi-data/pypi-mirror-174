""" pynchon.bin.cli
"""
import pynchon
from pynchon import (util,)

from .common import *
from pynchon.bin import (groups, options)
LOGGER = pynchon.get_logger(__name__)
PARENT = groups.gen_cli
@kommand(
    name='toc', parent=PARENT,
    formatters=dict(markdown=pynchon.T_TOC_CLI),
    options=[
        options.file_setupcfg, options.format,
        click.option(
            '--output', '-o', default='docs/cli/README.md',
            help=('output file to write.  (optional)')),
        options.stdout, options.header])
def toc(format, file, stdout, output, header):
    """
    Describe entrypoints for this project (parses setup.cfg)
    """
    return util.load_entrypoints(
            util.load_setupcfg(file=file))

@kommand(
    name='all', parent=PARENT,
    # formatters=dict(markdown=pynchon.T_DETAIL_CLI),
    options=[ options.file_setupcfg,
        # options.format,
        click.option(
            '--output-dir', default='docs/cli',
            help=('output directory (optional)')),
        options.stdout,])
def _all(
    # format,
        file, stdout, output_dir, ):
    """
    Generates help for every entrypoint
    """
    conf = util.load_entrypoints(
            util.load_setupcfg(file=file))
    entrypoints = conf['entrypoints']
    docs = {}
    for e in entrypoints:
        bin_name = str(e['bin_name'])
        epoint = e['setuptools_entrypoint']
        fname = os.path.join(output_dir, bin_name)
        fname = f"{fname}.md"
        LOGGER.debug(f"{epoint}: -> `{fname}`")
        docs[fname] = {
            **_entrypoint_docs(name=e['setuptools_entrypoint']),
            **e }
    for fname in docs:
        with open(fname,'w') as fhandle:
            fhandle.write(
                pynchon.T_DETAIL_CLI.render(
                    docs[fname]))
        LOGGER.debug(f"wrote: {fname}")
    return list(docs.keys())

@kommand(
    name='entrypoint', parent=PARENT,
    formatters=dict(markdown=pynchon.T_DETAIL_CLI),
    options=[
        options.format_markdown, options.stdout,
        options.header, options.file,
        options.output,
        options.name, options.module,
        ])
def entrypoint_docs(
    format, module, file, output,
    stdout, header, name):
    """
    Autogenenerate docs for python CLIs using click
    """
    tmp = _entrypoint_docs(module=module, name=name)
    return tmp

def _entrypoint_docs(module=None, name=None):
    """ """
    import importlib
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
    return dict(
        package=module.split('.')[0],
        module=module,
        entrypoint=name,
        commands=result,
    )

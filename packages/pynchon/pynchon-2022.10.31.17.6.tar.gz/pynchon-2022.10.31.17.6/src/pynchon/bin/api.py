""" pynchon.bin.api
"""
import click
import pynchon
from pynchon import (util,)
from .common import kommand
from pynchon.bin import (groups, options)
LOGGER = pynchon.get_logger(__name__)

def markdown(**result):
    return result['header'] + "\n".join(result['blocks'])

@kommand(name='toc', parent=groups.gen_api,
    formatters=dict(markdown=markdown),
    options=[options.format_markdown, options.package,
        click.option(
            '--output', '-o', default='docs/api/README.md',
            help=('output file to write.  (optional)')),
        options.file, options.stdout, options.header, ])
def toc(package, file, output, format, stdout, header):
    """
    Generate table-of-contents
    """

    module = util.get_module(package=package, file=file)
    result = util.visit_module(module=module, module_name=package)
    return dict(
        header=f"## API for '{package}' package\n\n{header}\n\n" + '-' * 80,
        blocks=result)

""" pynchon.bin.options
"""
import os
import sys
import click
import pynchon
LOGGER = pynchon.get_logger(__name__)

header = click.option(
    '--header', default='',
    help=('header to prepend output with. (optional)'))
name = click.option(
    '--name', default='',
    help=('name to use'))
stdout=click.option(
    '--stdout', is_flag=True, default=True,
    help=('whether to write to stdout.'))
output = click.option(
    '--output', '-o', default='',
    help=('output file to write.  (optional)'))
format = format_json = click.option(
    '--format', default='json',
    help=('output format to write'))
format_markdown = click.option(
    '--format', default='markdown',
    help=('output format to write'))
file = click.option(
    '--file', '-f', default='',
    help=('file to read as input'))
stdout=click.option(
    '--stdout', is_flag=True, default=True,
    help=('whether to write to stdout.'))
output = click.option(
    '--output', '-o', default='',
    help=('output file to write.  (optional)'))
format = click.option(
    '--format', '-m', default='json',
    help=('output format to write'))
package = click.option(
    '--package', '-p', default=os.environ.get('PY_PKG', '')
)
file_setupcfg = click.option(
    '--file', '-f', default='setup.cfg',
    help=('file to grab entrypoints from'))
module=click.option('--module', '-m', default='',
    help=(
        'module to grab click-cli from. '
        '(must be used with `name`)'))

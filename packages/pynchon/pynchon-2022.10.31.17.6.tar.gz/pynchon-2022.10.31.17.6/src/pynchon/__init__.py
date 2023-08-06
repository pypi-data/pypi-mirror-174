""" pynchon
"""
import os
import sys
import inspect
import importlib
import logging

import click
import jinja2

# NB: this should have been set by CI immediately
# before pypi-upload.  but the `except` below might
# be triggered by local development.
try:
    from ._version import __version__
except ImportError:
    __version__='0.0.0+local'

URL_BUILTINS = "https://docs.python.org/3/library/functions.html"

TEMPLATE_DIR = os.environ.get(
    'PYNCHON_TEMPLATE_DIR',
    os.path.join(
        os.path.dirname(__file__),
        'templates',))
assert os.path.exists(TEMPLATE_DIR), TEMPLATE_DIR

ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

T_DETAIL_CLI = ENV.get_template('cli/detail.md.j2')
T_TOC_API = ENV.get_template('api/TOC.md.j2')
T_TOC_CLI = ENV.get_template('cli/TOC.md.j2')


def get_logger(name):
    """
    utility function for returning a logger
    with standard formatting patterns, etc
    """
    if sys.stdout.isatty():
        import coloredlogs
        FormatterClass = coloredlogs.ColoredFormatter
    else:
        FormatterClass = logging.Formatter
    formatter = FormatterClass(
        fmt=' - '.join([
            "%(levelname)s",
            "%(name)s",
            "%(message)s"]),
        datefmt="%Y-%m-%d %H:%M:%S")
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    if not logger.handlers:
        # prevents duplicate registration
        logger.addHandler(log_handler)
    # FIXME: get this from some kind of global config
    logger.setLevel('DEBUG')
    # intermittent duplicated stuff without this
    logger.propagate = False
    return logger

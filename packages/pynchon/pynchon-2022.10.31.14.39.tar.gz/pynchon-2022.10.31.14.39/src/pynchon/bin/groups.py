""" pynchon.bin.groups
"""
import click

class group(object):

    def __init__(self, name=None, group=None, parent=None,):
        self.name=name
        self.parent = parent
        self.group = group or (self.parent.group if parent else click.group)

    def wrapper(self, *args, **kargs):
        result = self.fxn(*args, **kargs)
        return result

    def __call__(self, fxn):
        self.fxn = fxn
        return self.group(self.name)(self.wrapper)

@click.version_option()
@click.group('pynchon')
def entry():
    """ pynchon CLI: """
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    # ctx.ensure_object(dict)

@group('gen', parent=entry)
def gen():
    """ Generate docs """

@group('api', parent=gen)
def gen_api():
    """
    Generate API docs from python modules, packages, etc
    """

@group('cli',parent=gen)
def gen_cli():
    """ Generate CLI docs """

@group('project',parent=entry)
def project():
    """ Inspect project"""

@group('ast',parent=entry)
def ast():
    """ Inspect AST """

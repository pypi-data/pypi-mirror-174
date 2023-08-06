""" pynchon.util
"""
import os
import sys
import ast

import mccabe
import griffe

import pynchon
LOGGER = pynchon.get_logger(__name__)
from pynchon import annotate

LOGGER = pynchon.get_logger(__name__)
WORKING_DIR = os.getcwd()

def load_setupcfg(file:str='setup.cfg'):
    """ """
    import configparser
    config = configparser.ConfigParser()
    config.read(file)
    return config

def load_entrypoints(config=None):
    """ """
    console_scripts = config['options.entry_points']['console_scripts']
    console_scripts = [x for x in console_scripts.split('\n') if x ]
    package = config['metadata']['name']
    return dict(
        package=package,
        entrypoints=[dict(
            package=package,
            bin_name=c.split('=')[0].strip(),
            module=c.split('=')[1].strip().split(':')[0],
            entrypoint=c.split('=')[1].strip().split(':')[1],
            ) for c in console_scripts],)

def click_recursive_help(cmd,
    parent=None, out={}, file=sys.stdout):
    """ source: adapted from https://stackoverflow.com/questions/57810659/automatically-generate-all-help-documentation-for-click-commands """
    from click.core import Context as ClickContext
    full_name = cmd.name
    _parent = getattr(cmd, 'parent', None)
    ctx = ClickContext(cmd, info_name=cmd.name, parent=parent)
    out = {
        **out,
        **{full_name: cmd.get_help(ctx)}
    }
    commands = getattr(cmd, 'commands', {})
    for sub in commands.values():
        out ={**out, **click_recursive_help(sub, ctx)}
    return out

def get_module(package:str='', file:str=''):
    """ """
    if not bool(package) ^ bool(file):
        err = 'Expected --file or --package, but not both'
        raise RuntimeError(err)
    if file:
        file = os.path.abspath(file)
        new_path = os.path.dirname(file)
        assert os.path.exists(file)
        LOGGER.warning(f"modifying sys.path to include {new_path}")
        sys.path.append(new_path)
        package = os.path.splitext(os.path.basename(file))[0]
        working_dir = os.path.dirname(file)
    else:
        working_dir = WORKING_DIR
    loader = griffe.loader.GriffeLoader()
    module = loader.load_module(package)
    annotate.module(package, module, working_dir=working_dir)
    return module

def get_refs(working_dir=None, module=None) -> dict:
    """ """
    refs = dict(
        classes=dict([[k, v] for k, v in module.classes.items() if not module.classes[k].is_alias]),
        modules=dict([[k, v] for k, v in module.modules.items() if not module.modules[k].is_alias]),
        functions=dict([[k, v] for k, v in module.functions.items() if not module.functions[k].is_alias]),
    )
    for name,kls in refs['classes'].items():
        annotate.klass(name, kls)
    for name,mod in refs['modules'].items():
        annotate.module(name, mod, working_dir=working_dir)
    for name,fxn in refs['functions'].items():
        annotate.function(name, fxn)
    return refs

def visit_module(
        output=[], stats={}, module=None, template=pynchon.T_TOC_API,
        visited=[], module_name=None, working_dir=WORKING_DIR):
    """ recursive visitor for this package, submodules, classes, functions, etc """
    annotate.module(module_name, module, working_dir=working_dir)
    refs = get_refs(working_dir=working_dir, module=module)
    LOGGER.debug(f"rendering module: {module_name}")
    rendered = template.render(
        griffe=griffe, stats=stats,
        working_dir=working_dir,
        module_name=module_name, module=module,
        **refs)
    output.append(clean_text(rendered))
    for name, sub in refs['modules'].items():
        if sub in visited:
            continue
        visit_module(
            output=output, module=sub,
            working_dir=working_dir,
            module_name=f"{module_name}.{name}",
            visited=visited+[module],
            template=template)
    return output


def clean_text(txt:str) -> str:
    """ """
    return '\n'.join([
        line for line in txt.split('\n') if line.strip() ])

class Checker(mccabe.McCabeChecker):
    """ """

    def run(self):
        if self.max_complexity < 0:
            return
        visitor = mccabe.PathGraphingAstVisitor()
        visitor.preorder(self.tree, visitor)
        for graph in visitor.graphs.values():
            tmp=graph.complexity()
            if tmp > self.max_complexity:
                text = self._error_tmpl % (graph.entity, tmp)
                yield tmp, graph.lineno, graph.column, text, type(self)

def complexity(code:str=None, fname:str=None, threshold:int=7):
    """ """
    threshold=7
    try:
        tree = compile(code, fname, "exec", ast.PyCF_ONLY_AST)
    except SyntaxError:
        e = sys.exc_info()[1]
        sys.stderr.write("Unable to parse %s: %s\n" % (fname, e))
        return 0
    complex = []
    Checker.max_complexity = threshold
    for complexity, lineno, offset, text, check in Checker(tree, fname).run():
        complex.append(dict(
            file=os.path.relpath(fname),lineno=lineno,
            # text=text,
            score=complexity))
    out = []
    for admonition in complex:
        out.append(dict(
            glyph='🐉 Complex',
            hover=f'score {admonition["score"]} / {threshold}',
            link=f'/{admonition["file"]}#L{admonition["lineno"]}'))
    return out

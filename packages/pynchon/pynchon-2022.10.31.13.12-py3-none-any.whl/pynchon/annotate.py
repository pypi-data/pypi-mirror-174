""" """
import os
import sys
import inspect
import importlib
import pynchon
from pynchon import util
LOGGER = pynchon.get_logger(__name__)

def klass(name, kls) -> None:
    """ annotates a class """
    LOGGER.debug(f"annotating class: {name} {kls}")
    mod = importlib.import_module(kls.parent.canonical_path)
    kls._handle = getattr(mod, name)

    properties = []
    for x in dir(kls._handle):
        if x.startswith('_'):
            continue
        prop = getattr(kls._handle,x)
        is_property = type(prop).__name__=='property'
        if not is_property:
            continue
        fxn = prop.fget
        fxn_sig, fxn_doc = inspect.signature(fxn), fxn.__doc__ or ''
        try:
            fxn_code = fxn.__code__
        except AttributeError: # C extensions..
            fxn_code = None
        start = fxn_code.co_firstlineno if fxn_code else kls.lineno
        properties.append(dict(
            name=x,
            doc=fxn_doc,
            signature=fxn_sig,
            start=str(start),
            end='', # FIXME
            annotation=str(fxn_sig.return_annotation).replace("<class '","").replace("'>",""),
            fixme='FIXME' in fxn_doc))

    bases = []
    for x in kls._handle.__bases__:
        tmp = "[{name}]({link})"
        qname = x.__module__.replace('.', '')
        bname = x.__name__
        if 'builtin' in qname:
            tmp = tmp.format(
                name=f"`__builtin__.{bname}`",
                link=f"{pynchon.URL_BUILTINS}#func-{bname}")
        else:
            tmp = tmp.format(name=bname, link=f"#{qname}")
        bases.append(tmp)

    kls_code=inspect.getsource(kls._handle)
    kls_fname=inspect.getfile(kls._handle)
    kls._metadata=dict(
        bases=bases, code=kls_code,
        start=str(kls.lineno),
        end=str(kls.endlineno or ''),
        properties=properties)

    kls._metadata.update(mccabe=util.complexity(kls_code, kls_fname))

def module(name, module, working_dir=None) -> None:
    """ annotates a module """
    LOGGER.debug(f"annotating mod: {name} {module}")
    module._metadata = dict(
        base_url = str(module.filepath.relative_to(working_dir)))

def function(name, fxn) -> None:
    """ annotates a function """
    LOGGER.debug(f"annotating fxn: {name} {fxn}")
    mod = importlib.import_module(fxn.parent.canonical_path)
    handle = getattr(mod, name)
    fxn._handle = getattr(mod,name)
    fxn_doc = fxn._handle.__doc__ or ''
    try:
        fxn_fname = inspect.getfile(fxn._handle)
    except (Exception,) as exc:
        fxn_fname = '?'
        fxn_code = None
    else:
        fxn_fname = os.path.relpath(fxn_fname)
        fxn_code = inspect.getsource(fxn._handle)
    try:
        fxn_sig = inspect.signature(fxn._handle)
    except (Exception,) as exc:
        fxn_sig = None
    fixme_lines = [ i+fxn.lineno for i,l in enumerate(fxn_doc.split('\n')) if 'FIXME' in l]
    fxn._metadata = dict(
            name=name,
            doc=fxn_doc,
            signature=fxn_sig,
            # start=str(fxn._handle.__code__.co_firstlineno),
            annotation=str(fxn_sig and fxn_sig.return_annotation or '').replace("<class '","").replace("'>",""),
            fixme= [ dict(
                glyph=' 🚩has FIXMEs ',
                link=f'/{fxn_fname}#L{fixme_lines[0]}',
                hover=f"on lines {fixme_lines}") ] if fixme_lines else [])
    fxn_code and fxn._metadata.update(mccabe=util.complexity(fxn_code, fxn_fname))
    # logger.debug(exc)

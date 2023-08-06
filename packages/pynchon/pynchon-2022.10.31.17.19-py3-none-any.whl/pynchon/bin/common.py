""" pynchon.bin.common
"""
import os
import sys
import json
import functools

import click

import pynchon
LOGGER = pynchon.get_logger(__name__)


class handler(object):
    """ """

    priority = -1

    def __init__(self, parent=None):
        self.parent = parent
        self.logger = pynchon.get_logger(self.__class__.__name__)

    def match(self, call_kwargs):
        """ """
        return False

    def __call__(self, result, **call_kwargs):
        """ """
        return self.handle(result,**call_kwargs)

class stdout_handler(handler):
    """ """
    priority = 9

    def match(self, kwargs):
        """ """
        return 'stdout' in kwargs and kwargs['stdout']

    def handle(self, result,**call_kwargs):
        """ """
        print(result, file=sys.stdout)

class output_handler(handler):
    """ """

    priority = 10

    def match(_, kwargs):
        """ """
        return 'output' in kwargs and kwargs['output']

    def handle(self, result, output=None, **call_kwargs) -> None:
        """ """
        self.logger.debug(f"Saving to file: {output}")
        with open(output, 'w') as fhandle:
            fhandle.write(result)

class format_handler(handler):
    """ """
    def match(_, kwargs):
        """ """
        return 'format' in kwargs and kwargs['format']

    def transform(self, result, format:str=None, **call_kwargs):
        """ """
        if format.lower()=='json':
            warning = "JSON used for `format`; header will be ignored"
            self.logger.warning(warning)
            msg = self.parent.formatters[format](result)
        elif format=='markdown':
            fmt = self.parent.formatters[format]
            if not callable(fmt):
                template=fmt
                def fmt( **kargs):
                    return template.render({**kargs, **result})
            self.logger.debug(f"Dispatching formatter for `markdown` @ {fmt.__name__}")
            msg = fmt(**result)
            return msg
        else:
            err=f"Unsupported mode for `format`: {format}"
            self.logger.critical(err)
            raise ValueError(err)
        self.logger.debug(f"Transform output: {type(msg)}")
        return msg

class kommand(object):
    """ """

    def __init__(self, name=None, parent=None, options=[], transformers=[], handlers=[], formatters={}):
        """ """
        self.name = name
        self.parent = parent or click
        self.options = options
        self.formatters = {
            **formatters,
            **dict(json = self.format_json)
        }
        self.transformers = sorted(transformers + [
            format_handler(parent=self),
        ], key=lambda t: t.priority)
        self.handlers = sorted(handlers + [
            output_handler(parent=self),
            stdout_handler(parent=self),
        ], key=lambda h: h.priority)

        self.cmd = self.parent.command(self.name)
        self.logger=pynchon.get_logger(f'cmd[{name}]')

    def format_json(self, result):
        """ """
        self.logger.debug("Formatter for: `json`")
        return json.dumps(result, indent=2)

    def wrapper(self, *args, **call_kwargs):
        """ """
        @functools.wraps(self.fxn)
        def newf(*args, **call_kwargs):
            self.logger.debug(f"Invoking {self.parent.name}.{self.name}")
            self.logger.debug(f" with: {call_kwargs}")
            result = self.fxn(*args, **call_kwargs)
            for tformer in self.transformers:
                if tformer.match(call_kwargs):
                    result = tformer.transform(result, **call_kwargs)
            for handler in self.handlers:
                if handler.match(call_kwargs):
                    self.logger.debug(f"Handling with `{handler.__class__.__name__}`")
                    handler.handle(result, **call_kwargs)
            return result
        return newf

    def __call__(self, fxn):
        """ """
        self.fxn = fxn
        f = self.cmd(self.wrapper())
        for opt in self.options:
            f = opt(f)
        return f

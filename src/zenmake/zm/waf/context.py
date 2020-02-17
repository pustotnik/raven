# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os
import sys
from importlib import import_module as importModule

from waflib import Context as WafContextModule
from waflib.Context import Context as WafContext
from waflib.ConfigSet import ConfigSet
from zm import ZENMAKE_DIR, WAF_DIR
from zm.autodict import AutoDict as _AutoDict
from zm import utils, error
from zm.waf import wscriptimpl

joinpath = os.path.join

DEFAULT_TOOLDIRS = [
    joinpath(ZENMAKE_DIR, 'zm', 'tools'),
    joinpath(ZENMAKE_DIR, 'waf', 'waflib', 'Tools'),
    joinpath(ZENMAKE_DIR, 'waf', 'waflib', 'extras'),
]

def ctxmethod(ctxClass, methodName = None, wrap = False):
    """
    Decorator to replace/attach method to existing Waf context class
    """

    def decorator(func):
        funcName = methodName if methodName else func.__name__
        if wrap:
            method = getattr(ctxClass, funcName)
            def execute(*args, **kwargs):
                method(*args, **kwargs)
                func(*args, **kwargs)
            setattr(ctxClass, funcName, execute)
        else:
            setattr(ctxClass, funcName, func)
        return func

    return decorator

# Context is the base class for all other context classes and it is not auto
# registering class. So it cannot be just declared for extending/changing.

@ctxmethod(WafContext, 'getbconf')
def _getCtxBuildConf(ctx):
    return ctx.bconfManager.config(ctx.path.abspath())

@ctxmethod(WafContext, 'zmcache')
def _getLocalCtxCache(ctx):
    #pylint: disable=protected-access
    try:
        return ctx._zmcache
    except AttributeError:
        pass

    ctx._zmcache = _AutoDict()
    return ctx._zmcache

@ctxmethod(WafContext, 'recurse')
def _contextRecurse(ctx, dirs, name = None, mandatory = True, once = True, encoding = None):
    #pylint: disable=too-many-arguments,unused-argument

    cache = ctx.zmcache().recurse

    for dirpath in utils.toList(dirs):
        if not os.path.isabs(dirpath):
            # absolute paths only
            dirpath = joinpath(ctx.path.abspath(), dirpath)

        dirpath = os.path.normpath(dirpath)
        bconf = ctx.bconfManager.config(dirpath)
        if not bconf:
            continue

        node = ctx.root.make_node(joinpath(dirpath, 'virtual-buildconf'))
        funcName = name or ctx.fun

        tup = (node, funcName)
        if once and tup in cache:
            continue

        cache[tup] = True
        ctx.pre_recurse(node)

        try:
            # try to get function for command
            func = getattr(wscriptimpl, funcName, None)
            if not func:
                if not mandatory:
                    continue
                errmsg = 'No function %r defined in %s' % \
                            (funcName, wscriptimpl.__file__)
                raise error.ZenMakeError(errmsg)
            # call function for command
            func(ctx)
        finally:
            ctx.post_recurse(node)

@ctxmethod(WafContext, 'getTaskPathNode')
def _getTaskPathNode(self, taskStartDir):

    cache = self.zmcache().ctxpath
    if taskStartDir in cache:
        return cache[taskStartDir]

    bconf = self.getbconf()
    taskPath = os.path.abspath(os.path.join(bconf.rootdir, taskStartDir))
    pathNode = self.root.make_node(taskPath)

    cache[taskStartDir] = pathNode
    return pathNode

@ctxmethod(WafContext, 'loadTasksFromFileCache')
def _loadTasksFromFileCache(ctx, cachefile):
    """
    Load cached tasks from config cache if it exists.
    """

    #pylint: disable = unused-argument

    key = 'zmtasks'

    result = {}
    try:
        env = ConfigSet()
        env.load(cachefile)
        if key in env:
            result = env[key]
    except EnvironmentError:
        pass

    return result

def loadTool(tool, tooldirs = None, withSysPath = True):
    """
    Alternative version of WafContextModule.load_tool
    """

    if tool == 'java':
        tool = 'javaw'
    else:
        tool = tool.replace('++', 'xx')

    oldSysPath = sys.path

    if not withSysPath:
        sys.path = []
        if not tooldirs:
            sys.path = [WAF_DIR]

    if not tooldirs:
        tooldirs = DEFAULT_TOOLDIRS
    sys.path = tooldirs + sys.path

    module = None
    try:
        module = importModule(tool)
        WafContext.tools[tool] = module
    except ImportError as ex:
        toolsSysPath = list(sys.path)
        ex.toolsSysPath = toolsSysPath
        # for Waf
        ex.waf_sys_path = toolsSysPath
        raise
    finally:
        sys.path = oldSysPath

    return module

def _wafLoadTool(tool, tooldir = None, ctx = None, with_sys_path = True):
    # pylint: disable = invalid-name, unused-argument
    return loadTool(tool, tooldir, with_sys_path)

WafContextModule.load_tool = _wafLoadTool

@ctxmethod(WafContext, 'loadTool')
def _loadToolWitFunc(ctx, tool, tooldirs = None, callFunc = None, withSysPath = True):

    module = loadTool(tool, tooldirs, withSysPath)
    func = getattr(module, callFunc or ctx.fun, None)
    if func:
        func(ctx)

    return module

@ctxmethod(WafContext, 'load')
def _loadTools(ctx, tools, *args, **kwargs):
    """ This function is for compatibility with Waf """

    # pylint: disable = unused-argument

    tools = utils.toList(tools)
    tooldirs = utils.toList(kwargs.get('tooldir', ''))
    withSysPath = kwargs.get('with_sys_path', True)
    callFunc = kwargs.get('name', None)

    for tool in tools:
        _loadToolWitFunc(ctx, tool, tooldirs, callFunc, withSysPath)

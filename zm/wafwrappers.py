# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os
from waflib import Options, Context, Configure, Scripting
from waflib.ConfigSet import ConfigSet
from zm import utils, log, assist

joinpath = os.path.join

# Force to turn off internal WAF autoconfigure decorator.
# It's just to rid of needless work and to save working time.
Configure.autoconfig = False

def _areFilesChanged(bconfPaths):
    zmCmn = ConfigSet()
    try:
        zmcmnfile = bconfPaths.zmcmnfile
        zmCmn.load(zmcmnfile)
    except EnvironmentError:
        return True

    _hash = 0
    for file in zmCmn.monitfiles:
        try:
            _hash = utils.mkHashOfStrings((_hash, utils.readFile(file, 'rb')))
        except EnvironmentError:
            return True

    return _hash != zmCmn.monithash

def _areBuildTypesNotConfigured(clicmd, bconfHandler):
    buildconf = bconfHandler.conf
    buildtype = clicmd.args.buildtype
    zmcachedir = bconfHandler.confPaths.zmcachedir
    for taskName in buildconf.tasks:
        taskVariant = assist.getTaskVariantName(buildtype, taskName)
        fname = assist.makeCacheConfFileName(zmcachedir, taskVariant)
        if not os.path.exists(fname):
            return True
    return False

def _loadLockfileEnv(bconfPaths):
    env = ConfigSet()
    try:
        env.load(joinpath(bconfPaths.wscriptout, Options.lockfile))
    except EnvironmentError:
        return None
    return env

def _handleNoLockInTop(ctx, envGetter):

    if Context.top_dir and Context.out_dir:
        return False

    env = envGetter()
    if not env:
        if ctx.cmd != 'build':
            return True
        from zm.error import ZenMakeError
        raise ZenMakeError('The project was not configured: run "configure" '
                           'first or enable features.autoconfig in buildconf !')

    Context.run_dir = env.run_dir
    Context.top_dir = env.top_dir
    Context.out_dir = env.out_dir
    Scripting.run_command(ctx.cmd)
    return True

def wrapBldCtxNoLockInTop(bconfHandler, method):
    """
    Decorator that handles only case with conf.env.NO_LOCK_IN_RUN = True and/or
    conf.env.NO_LOCK_IN_TOP = True
    """

    def execute(self):
        bconfPaths = bconfHandler.confPaths
        if not _handleNoLockInTop(self, lambda: _loadLockfileEnv(bconfPaths)):
            method(self)

    return execute

def wrapBldCtxAutoConf(clicmd, bconfHandler, method):
    """
    Decorator that enables context commands to run *configure* as needed.
    It handles also case with conf.env.NO_LOCK_IN_RUN = True and/or
    conf.env.NO_LOCK_IN_TOP = True
    """

    def runConfigAndCommand(self, env):
        Scripting.run_command(env.config_cmd or 'configure')
        Scripting.run_command(self.cmd)

    def execute(self):

        wrapBldCtxAutoConf.callCounter += 1
        if wrapBldCtxAutoConf.callCounter > 10:
            # I some cases due to programming error, user actions or system
            # problems we can get infinite call of current function. Maybe
            # later I'll think up better protection but in normal case
            # it shouldn't happen.
            raise Exception('Infinite recursion was detected')

        # Execute the configuration automatically
        autoconfig = bconfHandler.conf.features['autoconfig']

        bconfPaths = bconfHandler.confPaths

        if not autoconfig:
            if not _handleNoLockInTop(self, lambda: _loadLockfileEnv(bconfPaths)):
                method(self)
            return

        env = _loadLockfileEnv(bconfPaths)
        if not env:
            log.warn('Configuring the project')
            runConfigAndCommand(self, ConfigSet())
            return

        if env.run_dir != bconfPaths.wscriptdir:
            runConfigAndCommand(self, env)
            return

        if _areFilesChanged(bconfPaths):
            runConfigAndCommand(self, env)
            return

        if _areBuildTypesNotConfigured(clicmd, bconfHandler):
            runConfigAndCommand(self, env)
            return

        if not _handleNoLockInTop(self, lambda: env):
            method(self)
        return

    return execute

wrapBldCtxAutoConf.callCounter = 0

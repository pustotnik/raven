# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

from waflib.ConfigSet import ConfigSet
from waflib.Build import BuildContext as WafBuildContext
from zm.pyutils import viewvalues
from zm.utils import asmethod
from zm import log, db
from zm.waf.assist import makeTasksCachePath
from zm.deps import produceExternalDeps

BuildContext = WafBuildContext

# WafBuildContext is used for many other waf commands as the base class
# and so to insert new methods into this class the decorator @asmethod is used.

@asmethod(WafBuildContext, 'load_envs', wrap = True, callOrigFirst = True)
def _loadEnvs(self):
    self.loadTasks()

@asmethod(WafBuildContext, 'loadTasks')
def _loadTasks(self):

    bconf = self.bconfManager.root
    buildtype = bconf.selectedBuildType
    cachedir = bconf.confPaths.zmcachedir
    cachePath = makeTasksCachePath(cachedir, buildtype)

    self.zmtasks = {}
    self.zmdepconfs = {}

    if not db.exists(cachePath):
        if self.cmd == 'clean':
            log.info("Buildtype '%s' not found. Nothing to clean" % buildtype)
            return

        self.fatal("Buildtype '%s' not found! Was step 'configure' missed?"
                   % buildtype)

    tasksData = db.loadFrom(cachePath)

    self.zmtasks = tasks = tasksData['tasks']
    taskenvs = tasksData['taskenvs']

    rootenv = self.all_envs['']
    for taskParams in viewvalues(tasks):
        taskVariant = taskParams['$task.variant']
        env = ConfigSet()
        env.table = taskenvs[taskVariant]
        env.parent = rootenv
        self.all_envs[taskVariant] = env

    self.zmdepconfs = tasksData['depconfs']

@asmethod(WafBuildContext, 'execute_build', wrap = True, callOrigFirst = False)
def _executeBuild(self):
    if self.cmd in ('build', 'install', 'uninstall', 'clean'):
        produceExternalDeps(self)
        log.printStep(self.cmd.capitalize() + 'ing')

@asmethod(WafBuildContext, 'validateVariant')
def _validateVariant(self):
    """ Check current variant and return it """

    if self.variant is None:
        self.fatal('No variant!')

    buildtype = self.variant
    return buildtype

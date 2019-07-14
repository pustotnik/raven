# coding=utf-8
#

# pylint: skip-file

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import sys
import os
import subprocess
import shutil
import pytest
import tests.common as cmn
import zm.utils
import zm.buildconfutil

joinpath = os.path.join

PLATFORM = zm.utils.platform()
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
ZM_BIN = os.path.normpath(joinpath(TESTS_DIR, os.path.pardir, "zenmake"))

# Copy projects into tmp dir
shutil.copytree(joinpath(TESTS_DIR, 'projects'), cmn.TEST_PROJECTS_DIR)

def collectProjectDirs():
    result = []
    for dirpath, _, filenames in os.walk(cmn.TEST_PROJECTS_DIR):
        if 'buildconf.py' in filenames:
            result.append(os.path.relpath(dirpath, cmn.TEST_PROJECTS_DIR))
    result.sort()
    return result

class TestProject(object):

    def _runZm(self, cmdline):
        timeout = 60 * 5
        proc = subprocess.Popen(cmdline, stdout = subprocess.PIPE,
                            stderr = subprocess.STDOUT, cwd = self.cwd,
                            env = os.environ.copy(), universal_newlines = True)
        if zm.utils.PY3:
            stdout, stderr = proc.communicate(timeout = timeout)
        else:
            stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            print('\n' + stdout)
        return proc.returncode

    @pytest.fixture(params = collectProjectDirs(), autouse = True)
    def setup(self, request):
        def teardown():
            pass

        request.addfinalizer(teardown)

        self.cwd = joinpath(cmn.TEST_PROJECTS_DIR, request.param)

    def testJustBuild(self, unsetEnviron):
        pythonbin = sys.executable
        if not pythonbin:
            pythonbin = 'python'
        cmdLine = [pythonbin, ZM_BIN, 'build']
        assert 0 == self._runZm(cmdLine)

# coding=utf-8
#

# pylint: skip-file

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os
import shutil
import pytest
import tests.common as cmn
from zm import utils

joinpath = os.path.join

class TestUtils(object):

    def testUnfoldPath(self):
        # it should be always absolute path
        cwd = os.getcwd()

        abspath = joinpath(cwd, 'something')
        relpath = joinpath('a', 'b', 'c')

        assert utils.unfoldPath(cwd, None) is None
        assert utils.unfoldPath(cwd, abspath) == abspath

        path = utils.unfoldPath(cwd, relpath)
        assert joinpath(cwd, relpath) == path
        assert os.path.isabs(utils.unfoldPath(abspath, relpath))

        os.environ['ABC'] = 'qwerty'

        assert joinpath(cwd, 'qwerty', relpath) == \
                        utils.unfoldPath(cwd, joinpath('$ABC', relpath))

    def testMkSymlink(self):
        destdir = joinpath(cmn.SHARED_TMP_DIR, 'test.util.mksymlink')
        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        os.makedirs(destdir)
        testfile = joinpath(destdir, 'testfile')
        with open(testfile, 'w+') as file:
            file.write("trash")

        symlink = joinpath(destdir, 'symlink')
        utils.mksymlink(testfile, symlink)
        assert os.path.islink(symlink)

        with pytest.raises(OSError):
            utils.mksymlink(testfile, symlink, force = False)

        utils.mksymlink(testfile, symlink, force = True)
        assert os.path.islink(symlink)

    def testToList(self):
        assert utils.toList('') == list()
        assert utils.toList('abc') == ['abc']
        assert utils.toList('a1 a2 b1 b2') == ['a1', 'a2', 'b1', 'b2']
        assert utils.toList(['a1', 'a2', 'b1']) == ['a1', 'a2', 'b1']

    def testNormalizeForFileName(self):
        assert utils.normalizeForFileName('abc') == 'abc'
        assert utils.normalizeForFileName(' abc ') == 'abc'
        assert utils.normalizeForFileName('a b c') == 'a_b_c'
        assert utils.normalizeForFileName('a b c', spaseAsDash = True) == 'a-b-c'
        assert utils.normalizeForFileName(' aBc<>:?*.e ') == 'aBc.e'
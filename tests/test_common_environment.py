# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import platform

import pytest
from minimock import Mock

from swid_generator.environments.common import CommonEnvironment


def test_os_string():
    platform.dist = Mock('platform.dist')
    platform.dist.mock_returns = ('debian', '7.4', '')
    assert CommonEnvironment.get_os_string() == 'debian_7.4'


@pytest.mark.skipif(sys.platform == 'win32', reason='requires windows')
def test_is_file(tmpdir):
    isfile = CommonEnvironment.is_file

    real_dir = tmpdir.mkdir('sub1')
    assert isfile(real_dir.strpath) is False, 'A directory is not a file.'

    fake_dir = tmpdir.join('sub2')
    assert isfile(fake_dir.strpath) is False, 'A nonexistant directory is not a file.'

    real_file = tmpdir.join('file1.txt')
    real_file.write('content')
    assert isfile(real_file.strpath) is True, 'Real file not recognized.'

    fake_file = tmpdir.join('file2.txt')
    assert isfile(fake_file.strpath) is False, 'A nonexistant file is not a file.'

    symlink = tmpdir.join('mysymlink')
    symlink.mksymlinkto(real_file)
    assert isfile(symlink.strpath) is True, 'A symlink is a file like object.'

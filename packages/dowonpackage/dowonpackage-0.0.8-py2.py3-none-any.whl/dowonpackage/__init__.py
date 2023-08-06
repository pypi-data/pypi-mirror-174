# -*- coding: utf-8 -*-
from __future__ import absolute_import

from dowonpackage.about import *

try:
    from dowonpackage.downloader import download
except IOError:
    pass

from dowonpackage.jvm import init_jvm

from dowonpackage import corpus
from dowonpackage import data
from dowonpackage import internals
from dowonpackage import tag


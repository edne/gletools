# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""
from __future__ import absolute_import

from . import framebuffer
from . import texture
from . import shader
from . import util

for module in [framebuffer, texture, shader, util]:
    locals().update({name: getattr(module, name)
                     for name in module.__all__})

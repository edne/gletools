# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

import framebuffer
import texture
import depthbuffer
import shader
import util

for module in [framebuffer, texture, depthbuffer, shader, util]:
    locals().update({name: getattr(module, name)
                     for name in module.__all__})

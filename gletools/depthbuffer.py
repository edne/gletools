# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from __future__ import with_statement
from __future__ import absolute_import

from ctypes import byref

import gletools.gl as gl
from .util import Context

__all__ = ['Depthbuffer']


class Depthbuffer(Context):
    _get = gl.GL_RENDERBUFFER_BINDING_EXT

    def bind(self, id):
        gl.glBindRenderbufferEXT(gl.GL_RENDERBUFFER_EXT, id)

    def __init__(self, width, height):
        Context.__init__(self)
        id = gl.GLuint()
        gl.glGenRenderbuffersEXT(1, byref(id))
        self.id = id.value
        with self:
            gl.glRenderbufferStorageEXT(gl.GL_RENDERBUFFER_EXT,
                                        gl.GL_DEPTH_COMPONENT,
                                        width, height)

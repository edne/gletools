# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from __future__ import with_statement
from __future__ import absolute_import

import gletools.gl as gl
from ctypes import byref
from .util import Context

__all__ = ['Texture']


class Object(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Texture(Context):
    specs = {gl.GL_RGBA: Object(type=Object(obj=gl.GLubyte,
                                            enum=gl.GL_UNSIGNED_BYTE),
                                channels=Object(enum=gl.GL_RGBA,
                                                count=4))}

    target = gl.GL_TEXTURE_2D

    _get = gl.GL_TEXTURE_BINDING_2D

    def bind(self, id):
        gl.glBindTexture(self.target, id)

    def _enter(self):
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TEXTURE_BIT)
        gl.glActiveTexture(self.unit)
        gl.glEnable(self.target)

    def _exit(self):
        gl.glPopAttrib()

    def __init__(self,
                 width, height,
                 format=gl.GL_RGBA, filter=gl.GL_LINEAR,
                 unit=gl.GL_TEXTURE0, data=None):
        Context.__init__(self)
        self.width = width
        self.height = height
        self.format = gl.GL_RGBA
        self.filter = gl.GL_LINEAR
        self.unit = unit
        self.spec = self.specs[gl.GL_RGBA]
        self.buffer_type = gl.GLubyte * (width*height * 4)
        id = self.id = gl.GLuint()

        gl.glGenTextures(1, byref(id))
        if data:
            self.buffer = self.buffer_type(*data)
        else:
            self.buffer = self.buffer_type()

        self.update()

    def set_data(self, data):
        with self:
            gl.glTexParameteri(self.target,
                               gl.GL_TEXTURE_MIN_FILTER,
                               self.filter)
            gl.glTexParameteri(self.target,
                               gl.GL_TEXTURE_MAG_FILTER,
                               self.filter)
            gl.glTexImage2D(
                self.target, 0, self.format,
                self.width, self.height,
                0,
                self.spec.channels.enum, self.spec.type.enum,
                data,
            )
            gl.glFlush()

    def update(self):
        self.set_data(self.buffer)

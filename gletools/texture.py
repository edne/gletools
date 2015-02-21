# -*- coding: utf-8 -*-

import gletools.gl as gl
from ctypes import byref
from .util import Context

__all__ = ['Texture']


class Texture(Context):
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
                 unit=gl.GL_TEXTURE0, data=None):
        Context.__init__(self)
        self.width = width
        self.height = height
        self.unit = unit
        self.buffer_type = gl.GLubyte * (width*height * 4)
        id = self.id = gl.GLuint()

        gl.glGenTextures(1, byref(id))
        if data:
            __buffer = self.buffer_type(*data)  # used only in scribble
        else:
            __buffer = self.buffer_type()

        with self:
            gl.glTexParameteri(self.target,
                               gl.GL_TEXTURE_MIN_FILTER,
                               gl.GL_LINEAR)
            gl.glTexParameteri(self.target,
                               gl.GL_TEXTURE_MAG_FILTER,
                               gl.GL_LINEAR)
            gl.glTexImage2D(
                self.target, 0, gl.GL_RGBA,
                self.width, self.height,
                0,
                gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
                __buffer,
            )
            gl.glFlush()

# -*- coding: utf-8 -*-

import gletools.gl as gl
from ctypes import byref

__all__ = ['SimpleTexture', 'Texture']


class SimpleTexture():
    def __init__(self, width, height):
        id = self.id = gl.GLuint()
        gl.glGenTextures(1, byref(id))

        # TODO generate with pyglet

        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TEXTURE_BIT)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glEnable(gl.GL_TEXTURE_2D)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.id)

        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,
                           gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D, 0, gl.GL_RGBA,
            width, height,
            0,
            gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
            (gl.GLubyte * (width*height * 4))(),
        )
        gl.glFlush()

        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glPopAttrib()


class Texture():
    target = gl.GL_TEXTURE_2D

    def __enter__(self):
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TEXTURE_BIT)
        gl.glActiveTexture(self.unit)
        gl.glEnable(self.target)

        gl.glBindTexture(self.target, self.id)

    def __exit__(self, foo1=None, foo2=None, foo3=None):
        gl.glBindTexture(self.target, 0)
        gl.glPopAttrib()

    def bind(self, id):
        gl.glBindTexture(self.target, id)

    def __init__(self,
                 width, height,
                 unit=gl.GL_TEXTURE0, data=None):

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

        self.__enter__()
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
        self.__exit__()

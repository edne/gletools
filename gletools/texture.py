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

    gl_byte = Object(
        obj=gl.GLubyte,
        enum=gl.GL_UNSIGNED_BYTE
    )
    gl_short = Object(
        obj=gl.GLushort,
        enum=gl.GL_UNSIGNED_SHORT
    )
    gl_float = Object(
        obj=gl.GLfloat,
        enum=gl.GL_FLOAT,
    )
    gl_half_float = Object(
        obj=gl.GLfloat,
        enum=gl.GL_FLOAT,
    )

    rgb = Object(
        enum=gl.GL_RGB,
        count=3,
    )
    rgba = Object(
        enum=gl.GL_RGBA,
        count=4,
    )
    luminance = Object(
        enum=gl.GL_LUMINANCE,
        count=1,
    )
    alpha = Object(
        enum=gl.GL_ALPHA,
        count=1,
    )

    specs = {
        gl.GL_RGB: Object(
            pil='RGB',
            type=gl_byte,
            channels=rgb,
        ),
        gl.GL_RGBA: Object(
            pil='RGBA',
            type=gl_byte,
            channels=rgba,
        ),
        gl.GL_RGB16: Object(
            type=gl_short,
            channels=rgb,
        ),
        gl.GL_RGBA32F: Object(
            pil='RGBA',
            type=gl_float,
            channels=rgba,
        ),
        gl.GL_RGB16F: Object(
            type=gl_half_float,
            channels=rgb,
        ),
        gl.GL_RGB32F: Object(
            pil='RGB',
            type=gl_float,
            channels=rgb,
        ),
        gl.GL_LUMINANCE32F: Object(
            pil='L',
            type=gl_float,
            channels=luminance,
        ),
        gl.GL_LUMINANCE: Object(
            type=gl_byte,
            channels=luminance,
        ),
        gl.GL_ALPHA: Object(
            type=gl_byte,
            channels=alpha,
        )
    }

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
        self.format = format
        self.filter = filter
        self.unit = unit
        spec = self.spec = self.specs[format]
        self.buffer_type = spec.type.obj * (width*height * spec.channels.count)
        id = self.id = gl.GLuint()

        gl.glGenTextures(1, byref(id))
        if data:
            self.buffer = self.buffer_type(*data)
        else:
            self.buffer = self.buffer_type()

        self.update()
        self.display = self.make_display()

    def make_display(self):
        uvs = 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0
        x1 = 0.0
        y1 = 0.0
        z = 0.0
        x2 = self.width
        y2 = self.height
        verts = (x1,    y1,    z,
                 x2,    y1,    z,
                 x2,    y2,    z,
                 x1,    y2,    z)

        return gl.pyglet.graphics.vertex_list(4,
                                              ('v3f', verts),
                                              ('t2f', uvs))

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

    def draw(self, x=0, y=0, z=0, scale=1.0):
        gl.glPushMatrix()
        gl.glTranslatef(x, y, z)
        with self:
            self.display.draw(gl.GL_QUADS)
        gl.glPopMatrix()

    def get_data(self, buffer):
        with self:
            gl.glPushClientAttrib(gl.GL_CLIENT_PIXEL_STORE_BIT)
            gl.glGetTexImage(
                self.target, 0, self.spec.channels.enum, self.spec.type.enum,
                buffer,
            )
            gl.glPopClientAttrib()

    def update(self):
        self.set_data(self.buffer)

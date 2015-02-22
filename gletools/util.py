# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""
from __future__ import with_statement
from __future__ import absolute_import

import gletools.gl as gl

__all__ = ['get',
           'Projection',
           'Screen']

_get_type_map = {
    int: (gl.GLint, gl.glGetIntegerv),
    float: (gl.GLfloat, gl.glGetFloatv),
}


def get(enum):
    values = (gl.GLint*1)()
    gl.glGetIntegerv(enum, values)
    return values[0]


class Context(object):
    def __init__(self):
        self.stack = list()

    def __enter__(self):
        self._enter()
        self.stack.append(get(self._get))
        self.bind(self.id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.check()
        id = self.stack.pop(-1)
        self.bind(id)
        self._exit()

    def _enter(self):
        pass

    def _exit(self):
        pass

    def check(self):
        pass


class MatrixMode(object):
    def __init__(self, mode):
        self.mode = mode

    def __enter__(self):
        gl.glPushAttrib(gl.GL_TRANSFORM_BIT)
        gl.glMatrixMode(self.mode)

    def __exit__(self, exc_type, exc_val, exc_tb):
        gl.glPopAttrib()


class Projection(object):
    def __init__(self, x, y, width, height, fov=55, near=0.1, far=100.0):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.fov = fov
        self.near, self.far = near, far

    def __enter__(self):
        gl.glPushAttrib(gl.GL_VIEWPORT_BIT)
        gl.glViewport(self.x, self.y, self.width, self.height)

        with MatrixMode(gl.GL_PROJECTION):
            gl.glPushMatrix()
            gl.glLoadIdentity()
            gl.gluPerspective(self.fov,
                              self.width / float(self.height),
                              self.near, self.far)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with MatrixMode(gl.GL_PROJECTION):
            gl.glPopMatrix()

        gl.glPopAttrib()


class Screen(object):
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def __enter__(self):
        gl.glPushAttrib(gl.GL_VIEWPORT_BIT)
        gl.glViewport(self.x, self.y, self.width, self.height)

        with MatrixMode(gl.GL_PROJECTION):
            gl.glPushMatrix()
            gl.glLoadIdentity()
            gl.gluOrtho2D(self.x, self.width, self.y, self.height)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with MatrixMode(gl.GL_PROJECTION):
            gl.glPopMatrix()

        gl.glPopAttrib()

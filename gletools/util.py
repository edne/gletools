# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""
from __future__ import with_statement

import gletools.gl as gl

__all__ = ['get',
           'Projection',
           'Screen',
           'Ortho',
           'Viewport',
           'Group',
           'interval',
           'quad',
           'Matrix',
           'DependencyException',
           'DepthTest',
           'SphereMapping',
           'Lighting']

_get_type_map = {
    int: (gl.GLint, gl.glGetIntegerv),
    float: (gl.GLfloat, gl.glGetFloatv),
}


def get(enum, size=1, type=int):
    type, accessor = _get_type_map[type]
    values = (type*size)()
    accessor(enum, values)
    if size == 1:
        return values[0]
    else:
        return values[:]


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


class Group(object):
    def __init__(self, *members, **named_members):
        self.__dict__.update(named_members)
        self._members = list(members) + named_members.values()

    def __enter__(self):
        for member in self._members:
            member.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        for member in reversed(self._members):
            member.__exit__(exc_type, exc_val, exc_tb)


class MatrixMode(object):
    def __init__(self, mode):
        self.mode = mode

    def __enter__(self):
        gl.glPushAttrib(gl.GL_TRANSFORM_BIT)
        gl.glMatrixMode(self.mode)

    def __exit__(self, exc_type, exc_val, exc_tb):
        gl.glPopAttrib()


class SphereMapping(object):
    @staticmethod
    def __enter__():
        gl.glPushAttrib(gl.GL_ENABLE_BIT | gl.GL_TEXTURE_BIT)
        gl.glTexGeni(gl.GL_S, gl.GL_TEXTURE_GEN_MODE, gl.GL_SPHERE_MAP)
        gl.glTexGeni(gl.GL_T, gl.GL_TEXTURE_GEN_MODE, gl.GL_SPHERE_MAP)
        gl.glEnable(gl.GL_TEXTURE_GEN_S)
        gl.glEnable(gl.GL_TEXTURE_GEN_T)

    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):
        gl.glPopAttrib()


class DepthTest(object):
    @staticmethod
    def __enter__():
        gl.glPushAttrib(gl.GL_DEPTH_BUFFER_BIT)
        gl.glEnable(gl.GL_DEPTH_TEST)

    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):
        gl.glPopAttrib()


class Lighting(object):
    @staticmethod
    def __enter__():
        gl.glPushAttrib(gl.GL_LIGHTING_BIT)
        gl.glEnable(gl.GL_LIGHTING)

    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):
        gl.glPopAttrib()


class Matrix(object):
    @staticmethod
    def __enter__():
        gl.glPushMatrix()

    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):
        gl.glPopMatrix()


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


class Viewport(object):
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def __enter__(self):
        gl.glPushAttrib(gl.GL_VIEWPORT_BIT)
        gl.glViewport(self.x, self.y, self.width, self.height)

    def __exit__(self, exc_type, exc_val, exc_tb):
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


class Ortho(object):
    def __init__(self, left, right, top, bottom, near, far):
        self.left, self.right = left, right
        self.top, self.bottom = top, bottom
        self.near, self.far = near, far

    def __enter__(self):
        with MatrixMode(gl.GL_PROJECTION):
            gl.glPushMatrix()
            gl.glLoadIdentity()
            gl.glOrtho(self.left, self.right,
                       self.bottom, self.top,
                       self.near, self.far)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with MatrixMode(gl.GL_PROJECTION):
            gl.glPopMatrix()


def interval(time):
    def _interval(fun):
        gl.pyglet.clock.schedule_interval(fun, time)
        return fun
    return _interval


def quad(left=-0.5, top=-0.5, right=0.5, bottom=0.5, scale=1.0):
    left *= scale
    right *= scale
    top *= scale
    bottom *= scale
    gl.glBegin(gl.GL_QUADS)
    gl.glTexCoord2f(1.0, 1.0)
    gl.glVertex3f(right, bottom, 0.0)
    gl.glTexCoord2f(1.0, 0.0)
    gl.glVertex3f(right, top, 0.0)
    gl.glTexCoord2f(0.0, 0.0)
    gl.glVertex3f(left, top, 0.0)
    gl.glTexCoord2f(0.0, 1.0)
    gl.glVertex3f(left, bottom, 0.0)
    gl.glEnd()


class DependencyException(Exception):
    pass

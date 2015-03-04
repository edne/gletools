# -*- coding: utf-8 -*-
from __future__ import with_statement
from __future__ import absolute_import

import pyglet
from gletools import (
    Projection, Framebuffer, Texture,
)
from gletools.gl import *

class Matrix(object):
    @staticmethod
    def __enter__():
        glPushMatrix()

    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):
        glPopMatrix()


class Group(object):
    def __init__(self, *members, **named_members):
        self.__dict__.update(named_members)
        self._members = list(members) + list(named_members.values())

    def __enter__(self):
        for member in self._members:
            member.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        for member in reversed(self._members):
            member.__exit__(exc_type, exc_val, exc_tb)



window = pyglet.window.Window()
projection = Projection(0, 0, window.width, window.height)
fbo = Framebuffer(
    Texture(window.width, window.height,
        data = [100,100,100,255]*(window.width*window.height)
    )
)


@fbo
def line(x0, y0, x1, y1):
    glBegin(GL_LINES)
    glVertex3f(x0, y0, 0)
    glVertex3f(x1, y1, 0)
    glEnd()


@window.event
def on_mouse_drag(x, y, rx, ry, button, modifier):
    if pyglet.window.mouse.LEFT == button:
        glColor4f(1,1,1,1)
        glLineWidth(3)
        line(x, y, x-rx, y-ry)



def interval(time):
    def _interval(fun):
        pyglet.clock.schedule_interval(fun, time)
        return fun
    return _interval


rotation = 0.0
@interval(0.03)
def simulate(delta):
    global rotation
    rotation += 40.0 * delta

 
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


@window.event
def on_draw():
    window.clear()
    with Group(fbo.textures[0], projection, Matrix):
        glTranslatef(0, 0, -3)
        glRotatef(-45, 1, 0, 0)
        glRotatef(rotation, 0.0, 0.0, 1.0)
        quad(scale=2)

if __name__ == '__main__':
    glEnable(GL_LINE_SMOOTH)
    pyglet.app.run()

# -*- coding: utf-8 -*-
import pyglet
from gletools import (
    Projection, Framebuffer, Texture,
)
import pyglet.gl as gl


class Matrix(object):
    @staticmethod
    def __enter__():
        gl.glPushMatrix()

    @staticmethod
    def __exit__(exc_type, exc_val, exc_tb):
        gl.glPopMatrix()


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


rotation = 0.0
window = pyglet.window.Window()
projection = Projection(0, 0, window.width, window.height)
fbo = Framebuffer(Texture(window.width, window.height,
                          data=[100, 100,
                                100, 255]*(window.width*window.height)))


def line(x0, y0, x1, y1):
    gl.glBegin(gl.GL_LINES)
    gl.glVertex3f(x0, y0, 0)
    gl.glVertex3f(x1, y1, 0)
    gl.glEnd()


@window.event
def on_mouse_drag(x, y, rx, ry, button, modifier):
    if pyglet.window.mouse.LEFT == button:
        gl.glColor4f(1, 1, 1, 1)
        gl.glLineWidth(3)
        with fbo:
            line(x, y, x-rx, y-ry)


def interval(time):
    def _interval(fun):
        pyglet.clock.schedule_interval(fun, time)
        return fun
    return _interval


@interval(0.03)
def simulate(delta):
    global rotation
    rotation += 40.0 * delta


@window.event
def on_draw():
    window.clear()
    with Group(fbo.textures[0], projection, Matrix):
        gl.glTranslatef(0, 0, -3)
        gl.glRotatef(-45, 1, 0, 0)
        gl.glRotatef(rotation, 0.0, 0.0, 1.0)

        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(1.0, 1.0)
        gl.glVertex3f(1, 1, 0.0)
        gl.glTexCoord2f(1.0, 0.0)
        gl.glVertex3f(1, -1, 0.0)
        gl.glTexCoord2f(0.0, 0.0)
        gl.glVertex3f(-1, -1, 0.0)
        gl.glTexCoord2f(0.0, 1.0)
        gl.glVertex3f(-1, 1, 0.0)
        gl.glEnd()

if __name__ == '__main__':
    gl.glEnable(gl.GL_LINE_SMOOTH)
    pyglet.app.run()

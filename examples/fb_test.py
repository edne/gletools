import pyglet
from gletools import SimpleTexture, SimpleFramebuffer
from gletools.gl import *
from pyglet.image import Texture

window = pyglet.window.Window()


def quad(min=0.0, max=1.0):
    glBegin(GL_QUADS)
    glColor3f(0, 1, 1)
    glVertex3f(max, max, 0.0)
    glVertex3f(max, min, 0.0)
    glColor3f(1, 1, 0)
    glVertex3f(min, min, 0.0)
    glVertex3f(min, max, 0.0)
    glEnd()

texture_old = SimpleTexture(64, 64)
framebuffer = SimpleFramebuffer(texture_old.id)
texture = Texture(64, 64, GL_TEXTURE_2D, texture_old.id)


@window.event
def on_draw():
    window.clear()
    with framebuffer:
        quad(0.0, 64)

    texture.blit(0, 0, 0, window.width, window.height)


if __name__ == '__main__':
    pyglet.app.run()

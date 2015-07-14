import pyglet
from gletools import SimpleFramebuffer
from gletools.gl import *

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

fb = SimpleFramebuffer(64, 64)
fb2 = SimpleFramebuffer(64, 64)


@window.event
def on_draw():
    window.clear()
    with fb:
        quad(0.0, 64)

    # fb.texture.blit(0, 0, 0, window.width, window.height)

    with fb2:
        fb.texture.blit(0, 0)
    fb2.texture.blit(0, 0)


if __name__ == '__main__':
    pyglet.app.run()

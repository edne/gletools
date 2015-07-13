import pyglet
from gletools import Texture, Framebuffer, Projection
from gletools.gl import *

window = pyglet.window.Window()
projection = Projection(0, 0, window.width, window.height)


def quad(min=0.0, max=1.0):
    glBegin(GL_QUADS)
    # glTexCoord2f(1.0, 1.0)
    glColor3f(0, 1, 1)
    glVertex3f(max, max, 0.0)
    # glTexCoord2f(1.0, 0.0)
    glVertex3f(max, min, 0.0)
    # glTexCoord2f(0.0, 0.0)
    glColor3f(1, 1, 0)
    glVertex3f(min, min, 0.0)
    # glTexCoord2f(0.0, 1.0)
    glVertex3f(min, max, 0.0)
    glEnd()

texture_old = Texture(64, 64)
from pyglet.image import Texture
# texture = Texture.create_for_size(GL_TEXTURE_2D, 64, 64)
framebuffer = Framebuffer(texture_old)
texture = Texture(64, 64, GL_TEXTURE_2D, texture_old.id)


@window.event
def on_draw():
    window.clear()
    with framebuffer:
        quad(0.0, 64)

    texture.blit(0, 0, 0, window.width, window.height)


if __name__ == '__main__':
    pyglet.app.run()

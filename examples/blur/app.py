from __future__ import with_statement
from __future__ import absolute_import

import pyglet
from gletools import (
    ShaderProgram, VertexShader, FragmentShader,
    Texture, Framebuffer, Sampler2D,
    Projection, Screen,
)
from gletools.gl import *

window = pyglet.window.Window()

framebuffer = Framebuffer(
    Texture(window.width, window.height),
    Texture(window.width, window.height),
    Texture(window.width, window.height, unit=GL_TEXTURE1),
)

depth_shader = VertexShader('''
    varying float depth;
    void main()
    {
        depth = -(gl_ModelViewMatrix * gl_Vertex).z;
        gl_Position = ftransform();
        gl_FrontColor = gl_Color;
    }

''')

blur = ShaderProgram(
    depth_shader,
    FragmentShader.open('shader.frag'),
)
blur.vars.width = float(window.width)
blur.vars.height = float(window.height)
blur.vars.texture = Sampler2D(GL_TEXTURE0)
blur.vars.depthmap = Sampler2D(GL_TEXTURE1)

depth = ShaderProgram(
    depth_shader,
    FragmentShader('''
        varying float depth;
        void main(){
            gl_FragData[0] = gl_Color;
            gl_FragData[1] = gl_Color;
            gl_FragData[2] = vec4(depth, depth, depth, 1.0);
        }
    '''),
)

rotation = 0.0


def quad(left, right, top, bottom):
    glBegin(GL_QUADS)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(right, top, 0.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(right, bottom, 0.0)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(left, bottom, 0.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(left, top, 0.0)
    glEnd()


def blur_geom():
    glPushMatrix()
    glRotatef(90, 1.0, 0.0, 0.0)
    quad(left=-0.5, right=0.5, top=1, bottom=-1)
    glPopMatrix()


def simulate(delta):
    global rotation
    rotation += 40.0 * delta

pyglet.clock.schedule_interval(simulate, 0.01)
projection = Projection(0, 0, window.width, window.height)
ortho = Screen(0, 0, window.width, window.height)


@window.event
def on_draw():
    window.clear()

    with projection:
        glPushMatrix()
        glTranslatef(0, 0, -3)
        glRotatef(-45, 1, 0, 0)
        glRotatef(rotation, 0.0, 0.0, 1.0)

        framebuffer.drawto(
            GL_COLOR_ATTACHMENT0_EXT, GL_COLOR_ATTACHMENT1_EXT, GL_COLOR_ATTACHMENT2_EXT)
        with framebuffer, depth:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glColor3f(0.0, 1.0, 0.0)
            quad(left=-1, right=1, top=1, bottom=-1)

        framebuffer.drawto(GL_COLOR_ATTACHMENT1_EXT)
        with framebuffer, blur, framebuffer.textures[2], framebuffer.textures[0]:
            glColor3f(1.0, 1.0, 1.0)
            blur_geom()
        glPopMatrix()

    with framebuffer.textures[1], ortho:
        glColor4f(1.0, 1.0, 1.0, 1.0)
        quad(left=0, right=window.width, top=window.height, bottom=0)

if __name__ == '__main__':
    glEnable(GL_DEPTH_TEST)
    pyglet.app.run()

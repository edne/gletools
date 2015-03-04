# -*- coding: utf-8 -*-

from ctypes import byref
import pyglet.gl as gl


__all__ = ['Framebuffer']


def getIntegerv(enum):
    values = (gl.GLint*1)()
    gl.glGetIntegerv(enum, values)
    return values[0]


class Framebuffer(object):
    _get = gl.GL_FRAMEBUFFER_BINDING_EXT

    def bind(self, id):
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, gl.GLuint(id))

    def __init__(self, *textures):
        if not gl.gl_info.have_extension('GL_EXT_framebuffer_object'):
            raise Exception('framebuffer object extension not available')

        # Context.__init__(self)
        self.stack = list()
        self.textures = [None] * getIntegerv(gl.GL_MAX_COLOR_ATTACHMENTS_EXT)

        id = gl.GLuint()
        gl.glGenFramebuffersEXT(1, byref(id))
        self.id = id.value

        self.textures = [None] * getIntegerv(gl.GL_MAX_COLOR_ATTACHMENTS_EXT)
        self.setTextures(*textures)

    def setTextures(self, *textures):
        for i, texture in enumerate(textures):
            with self:
                gl.glFramebufferTexture2DEXT(gl.GL_FRAMEBUFFER_EXT,
                                             gl.GL_COLOR_ATTACHMENT0_EXT + i,
                                             texture.target,
                                             texture.id,
                                             0)
                self.textures[i] = texture

    def depth(self, depth):
        with self:
            gl.glFramebufferRenderbufferEXT(gl.GL_FRAMEBUFFER_EXT,
                                            gl.GL_DEPTH_ATTACHMENT_EXT,
                                            gl.GL_RENDERBUFFER_EXT,
                                            depth.id)

    def drawto(self, *enums):
        with self:
            buffers = (gl.GLenum * len(enums))(*enums)
            gl.glDrawBuffers(len(enums), buffers)

    def __enter__(self):
        self.stack.append(getIntegerv(self._get))
        self.bind(self.id)

    def __exit__(self, exc_type, exc_val, exc_tb):
        id = self.stack.pop(-1)
        self.bind(id)

# -*- coding: utf-8 -*-

from ctypes import byref
import pyglet.gl as gl


__all__ = ['Framebuffer']


class Framebuffer(object):
    def __init__(self, *textures):
        if not gl.gl_info.have_extension('GL_EXT_framebuffer_object'):
            raise Exception('framebuffer object extension not available')

        framebuffer_id = gl.GLuint()
        gl.glGenFramebuffersEXT(1, byref(framebuffer_id))
        self.id = framebuffer_id.value

        self.setTextures(*textures)

    def setTextures(self, *textures):
        self.textures = []
        for i, texture in enumerate(textures):
            with self:
                gl.glFramebufferTexture2DEXT(gl.GL_FRAMEBUFFER_EXT,
                                             gl.GL_COLOR_ATTACHMENT0_EXT + i,
                                             gl.GL_TEXTURE_2D,
                                             texture.id,
                                             0)
                self.textures.append(texture)

    def drawto(self, *enums):
        with self:
            buffers = (gl.GLenum * len(enums))(*enums)
            gl.glDrawBuffers(len(enums), buffers)

    def __enter__(self):
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, gl.GLuint(self.id))

    def __exit__(self, exc_type, exc_val, exc_tb):
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, 0)

# -*- coding: utf-8 -*-

from ctypes import byref


import gletools.gl as gl
from .util import Context, get

__all__ = ['Framebuffer']


class Framebuffer(Context):
    _get = gl.GL_FRAMEBUFFER_BINDING_EXT

    def bind(self, id):
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, gl.GLuint(id))

    def __init__(self, *textures):
        if not gl.gl_info.have_extension('GL_EXT_framebuffer_object'):
            raise Exception('framebuffer object extension not available')

        Context.__init__(self)
        self.textures = [None] * get(gl.GL_MAX_COLOR_ATTACHMENTS_EXT)

        id = gl.GLuint()
        gl.glGenFramebuffersEXT(1, byref(id))
        self.id = id.value

        self.textures = [None] * get(gl.GL_MAX_COLOR_ATTACHMENTS_EXT)
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

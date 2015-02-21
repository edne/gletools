# -*- coding: utf-8 -*-

"""
    :copyright: 2009 by Florian Boesch <pyalot@gmail.com>.
    :license: GNU AGPL v3 or later, see LICENSE for more details.
"""

from __future__ import with_statement
from __future__ import absolute_import

from ctypes import byref


import gletools.gl as gl
from .util import Context, get

__all__ = ['Framebuffer']


class Textures(object):
    def __init__(self, framebuffer):
        self.framebuffer = framebuffer
        self.textures = [None] * get(gl.GL_MAX_COLOR_ATTACHMENTS_EXT)

    def __getitem__(self, i):
        return self.textures[i]

    def __setitem__(self, i, texture):
        with self.framebuffer:
            gl.glFramebufferTexture2DEXT(
                gl.GL_FRAMEBUFFER_EXT,
                gl.GL_COLOR_ATTACHMENT0_EXT + i,
                texture.target,
                texture.id,
                0,
            )
            self.textures[i] = texture

    def __iter__(self):
        return iter(self.textures)


class Framebuffer(Context):
    errors = {gl.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT:
              'GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT',

              gl.GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT:
              'GL_FRAMEBUFFER_INCOMPLETE_MISSING_ATTACHMENT_EXT: \
                      no image is attached',

              gl.GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT:
              'GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT: \
                      attached images dont have the same size',

              gl.GL_FRAMEBUFFER_INCOMPLETE_FORMATS_EXT:
              'GL_FRAMEBUFFER_INCOMPLETE_FORMATS_EXT: \
                      the attached images dont have the same format',

              gl.GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT:
              'GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT',

              gl.GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT:
              'GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT',

              gl.GL_FRAMEBUFFER_UNSUPPORTED_EXT:
              'GL_FRAMEBUFFER_UNSUPPORTED_EXT'}

    class Exception(Exception):
        pass

    _get = gl.GL_FRAMEBUFFER_BINDING_EXT

    def bind(self, id):
        gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, gl.GLuint(id))

    def __init__(self, *textures):
        if not gl.gl_info.have_extension('GL_EXT_framebuffer_object'):
            raise self.Exception('framebuffer object extension not available')

        Context.__init__(self)
        self._texture = None
        self._depth = None
        id = gl.GLuint()
        gl.glGenFramebuffersEXT(1, byref(id))
        self.id = id.value
        self._textures = Textures(self)
        for i, texture in enumerate(textures):
            self.textures[i] = texture

    def depth(self, depth):
        self._depth = depth
        with self:
            gl.glFramebufferRenderbufferEXT(
                gl.GL_FRAMEBUFFER_EXT,
                gl.GL_DEPTH_ATTACHMENT_EXT,
                gl.GL_RENDERBUFFER_EXT,
                depth.id,
            )

    def drawto(self, *enums):
        with self:
            buffers = (gl.GLenum * len(enums))(*enums)
            gl.glDrawBuffers(len(enums), buffers)

    def get_textures(self):
        return self._textures

    def set_textures(self, textures):
        for i, texture in enumerate(textures):
            self._textures[i] = texture

    textures = property(get_textures, set_textures)

from __future__ import absolute_import
import pyglet.gl as gl
import pyglet.gl.glext_arb as glext_arb


locals().update(gl.__dict__)


for constant in ['GL_RGBA32F',
                 'GL_RGB16F',
                 'GL_RGB32F',
                 'GL_LUMINANCE32F']:

    if not hasattr(gl, constant):
        locals()[constant] = getattr(glext_arb,
                                     constant + '_ARB')

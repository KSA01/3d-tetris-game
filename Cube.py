# Cube.py

from OpenGL.GL import *
import numpy as np
import math
import random

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

# 3 positions, 3 normals, 2 UVs
_verts = np.float32([(1, -1, -1, 0, 0, -1, 0, 0),   # first - 8 vertices x 3
                    (1, 1, -1, 0, 0, -1, 1, 0),
                    (-1, 1, -1, 0, 0, -1, 1, 1),
                    (-1, -1, -1, 0, 0, -1, 0, 1),

                    (-1, -1, -1, -1, 0, 0, 0, 0),
                    (-1, 1, -1, -1, 0, 0, 1, 0),
                    (-1, 1, 1, -1, 0, 0, 1, 1),
                    (-1, -1, 1, -1, 0, 0, 0, 1),

                    (-1, -1, 1, 0, 0, 1, 0, 0),    # second
                    (-1, 1, 1, 0, 0, 1, 1, 0),
                    (1, 1, 1, 0, 0, 1, 1, 1),
                    (1, -1, 1, 0, 0, 1, 0, 1),
                                  
                    (1, -1, 1, 1, 0, 0, 0, 0),
                    (1, 1, 1, 1, 0, 0, 1, 0),
                    (1, 1, -1, 1, 0, 0, 1, 1),
                    (1, -1, -1, 1, 0, 0, 0, 1),
                                  
                    (1, 1, -1, 0, 1, 0, 0, 0),   # third
                    (1, 1, 1, 0, 1, 0, 1, 0),
                    (-1, 1, 1, 0, 1, 0, 1, 1),
                    (-1, 1, -1, 0, 1, 0, 0, 1),
                                  
                    (1, -1, 1, 0, -1, 0, 0, 0),
                    (1, -1, -1, 0, -1, 0, 1, 0),
                    (-1, -1, -1, 0, -1, 0, 1, 1),
                    (-1, -1, 1, 0, -1, 0, 0, 1)
                    ])

colors = (
        [1,0,0], # Red 0
        [0,1,0], # Green 1
        [0,0,1], # Blue 2
        [1,1,0], # Yellow 3
        [0,1,1], # Cyan 4
        [1,0.5,0], # Orange 5
        [1,0,1]) # Purple 6

def Init():
    global _shader
    global _vbo
    global _verts
    global _uniformInv
    global _position
    global _color
    global _vertex_normal

    _VERTEX_SHADER = shaders.compileShader("""
        uniform mat4 inv;
        attribute vec3 position;
        uniform vec3 color;
        attribute vec3 vertex_normal;
        varying vec4 vertex_color;
        void main()
        {
            gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
            vec4 light = inv * vec4(0, 0, 1, 0);
            float dt = dot(light.xyz, vertex_normal);
            float mult = max(min(dt, 1.0), 0.0);
            vertex_color = vec4(color * mult, 1.0);
        }
    """, GL_VERTEX_SHADER)

    _FRAGMENT_SHADER = shaders.compileShader("""
        varying vec4 vertex_color;
        void main()
        {
            gl_FragColor = vertex_color;
        }
    """, GL_FRAGMENT_SHADER)

    _shader = shaders.compileProgram(_VERTEX_SHADER, _FRAGMENT_SHADER)
    _vbo = vbo.VBO(_verts)

    _uniformInv = glGetUniformLocation(_shader, "inv")
    _position = glGetAttribLocation(_shader, "position")
    _color = glGetUniformLocation(_shader, "color")
    _vertex_normal = glGetAttribLocation(_shader, "vertex_normal")

class Cube:
    def __init__(self, color, axis):
        super().__init__()
        self.color = np.asfarray(color)
        self.ang = 0
        self.axis = axis

    def Update(self, deltaTime):
        self.ang += 50.0 * deltaTime

    def _DrawBlock(self):
        global _shader
        global _vbo
        global _verts
        global _uniformInv
        global _position
        global _color
        global _vertex_normal

        shaders.glUseProgram(_shader)

        inv = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX))
        glUniformMatrix4fv(_uniformInv, 1, False, inv)
        glUniform3fv(_color, 1, self.color)

        try:
            _vbo.bind()
            try:
                glEnableVertexAttribArray(_position)
                glEnableVertexAttribArray(_vertex_normal)
                stride = 32
                glVertexAttribPointer(_position, 3, GL_FLOAT, False, stride, _vbo)
                glVertexAttribPointer(_vertex_normal, 3, GL_FLOAT, True, stride, _vbo+12)
                glDrawArrays(GL_QUADS, 0, 24)
            finally:
                _vbo.unbind()
                glDisableVertexAttribArray(_position)
                glDisableVertexAttribArray(_vertex_normal)
        finally:
            shaders.glUseProgram(0)

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glRotatef(self.ang, *self.axis)
        self._DrawBlock()

        #glLoadMatrixf(m)
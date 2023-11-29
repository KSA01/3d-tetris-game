# Cube.py

from OpenGL.GL import *
import numpy as np
from math import *
import random

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

import pygame
from Texture import Texture

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

def Init():
    global _shader
    global _vbo
    global _verts
    global _uniformInv
    global _position
    global _color
    global _vertex_normal

    global _uv_coords

    _VERTEX_SHADER = shaders.compileShader("""
        uniform mat4 inv;
        attribute vec3 position;
        uniform vec3 color;
        attribute vec3 vertex_normal;
        varying vec4 vertex_color;
                                           
        attribute vec2 inTexCoord;
        varying vec2 vertexTexCoord;
                                           
        void main()
        {
            gl_Position = gl_ModelViewProjectionMatrix * vec4(position, 1.0);
            vec4 light = inv * vec4(0, 0, 1, 0);
            float dt = dot(light.xyz, vertex_normal);
            float mult = max(min(dt, 1.0), 0.0);
            vertex_color = vec4(color * mult, 1.0);
                                           
            vertexTexCoord = inTexCoord;
        }
    """, GL_VERTEX_SHADER)

    _FRAGMENT_SHADER = shaders.compileShader("""
        varying vec4 vertex_color;
                                             
        varying vec2 vertexTexCoord;
        uniform sampler2D myTex;
                                             
        void main()
        {
            gl_FragColor = texture(myTex, vertexTexCoord) * vertex_color;
        }
    """, GL_FRAGMENT_SHADER)

    _shader = shaders.compileProgram(_VERTEX_SHADER, _FRAGMENT_SHADER)
    _vbo = vbo.VBO(_verts)

    _uniformInv = glGetUniformLocation(_shader, "inv")
    _position = glGetAttribLocation(_shader, "position")
    _color = glGetUniformLocation(_shader, "color")
    _vertex_normal = glGetAttribLocation(_shader, "vertex_normal")

    _uv_coords = glGetAttribLocation(_shader, "inTexCoord")

class Cube:
    def __init__(self, localPos, color=([0,0,1]), filepath="blueberryI.png"):
        #super().__init__()
        self.color = np.asfarray(color)
        self.ang = 0
        self.axis = (3,1,1)
        self.localPos = localPos   # Takes local positions of the current cube from pieces

        self.filepath = filepath

        #Generate the texture
        self.fruit_texture = Texture(self.filepath)

    def GetCubePos(self):
        return self.localPos

    def SetCubePos(self, newPos):
        self.localPos = newPos

    # Rotation function for cube
    '''def Rotate(self, quaternion):
        # Rotate the local position of the cube using quaternion multiplication
        rotated_position = q_mult(q_mult(quaternion, np.concatenate(([0], self.localPos))), q_conjugate(quaternion))[1:]
        self.localPos = rotated_position'''

    def Update(self, deltaTime, move):
        self.ang += 50.0 * deltaTime
        self.localPos += move

    def _DrawBlock(self):
        global _shader
        global _vbo
        global _verts
        global _uniformInv
        global _position
        global _color
        global _vertex_normal
        global _uv_coords

        
        #Set the texture of the block
        self.fruit_texture.use()


        shaders.glUseProgram(_shader)

        inv = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX))
        glUniformMatrix4fv(_uniformInv, 1, False, inv)
        glUniform3fv(_color, 1, self.color)

        try:
            _vbo.bind()
            try:
                glEnableVertexAttribArray(_position)
                glEnableVertexAttribArray(_vertex_normal)
                glEnableVertexAttribArray(_uv_coords)
                stride = 32
                glVertexAttribPointer(_position, 3, GL_FLOAT, False, stride, _vbo)
                glVertexAttribPointer(_vertex_normal, 3, GL_FLOAT, True, stride, _vbo+12)
                glVertexAttribPointer(_uv_coords, 2, GL_FLOAT, True, stride, _vbo+24)
                glDrawArrays(GL_QUADS, 0, 24)
            finally:
                _vbo.unbind()
                glDisableVertexAttribArray(_position)
                glDisableVertexAttribArray(_vertex_normal)
                glDisableVertexAttribArray(_uv_coords)
        finally:
            shaders.glUseProgram(0)
    
    #DIFF HERE

    def Render(self, scale_factor=0.75, block_spacing=0.25):  # Change these 2 values to adjust size
        #m = glGetDouble(GL_MODELVIEW_MATRIX)

        glPushMatrix()
        #glTranslatef(*self.localPos)     # Translates the local position of each cube from pieces.py
        glScalef(scale_factor, scale_factor, scale_factor)
        adjusted_translation = [pos * (scale_factor + block_spacing) for pos in self.localPos]
        glTranslatef(*adjusted_translation)
        #glRotatef(self.ang, *self.axis)
        self._DrawBlock()
        glPopMatrix()

        #glLoadMatrixf(m)

def normalize(v, tolerance=0.00001):
    mag2 = sum(n * n for n in v)
    if abs(mag2 - 1.0) > tolerance:
        mag = sqrt(mag2)
        v = tuple(n / mag for n in v)
    return v

def q_conjugate(q):
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return np.array([w, x, y, z])

def q_to_mat4(q):
    w, x, y, z = q
    return np.array(
        [[1 - 2*y*y - 2*z*z, 2*x*y - 2*z*w, 2*x*z + 2*y*w, 0],
        [2*x*y + 2*z*w, 1 - 2*x*x - 2*z*z, 2*y*z - 2*x*w, 0],
        [2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x*x - 2*y*y, 0],
        [0, 0, 0, 1] ],'f')

def axis_rotation_quaternion(angle, axis):
    axis = normalize(axis)
    angle /= 2
    w = cos(angle)
    x, y, z = [coord * sin(angle) for coord in axis]
    return w, x, y, z

def axis_rotation_matrix(angle, axis):
    axis = np.asarray(axis)
    axis = axis / np.sqrt(np.dot(axis, axis))
    q = np.array([np.cos(angle / 2.0), *(-axis * np.sin(angle / 2.0))])
    rotation_matrix = np.array([
        [1 - 2 * (q[2]**2 + q[3]**2), 2 * (q[1] * q[2] - q[0] * q[3]), 2 * (q[1] * q[3] + q[0] * q[2])],
        [2 * (q[1] * q[2] + q[0] * q[3]), 1 - 2 * (q[1]**2 + q[3]**2), 2 * (q[2] * q[3] - q[0] * q[1])],
        [2 * (q[1] * q[3] - q[0] * q[2]), 2 * (q[2] * q[3] + q[0] * q[1]), 1 - 2 * (q[1]**2 + q[2]**2)],
    ])
    return rotation_matrix

# rotation matrix quaternians
'''def axis_rotation_matrix(angle, axis):
        axis = np.asarray(axis)
        axis = axis / np.sqrt(np.dot(axis, axis))
        a = np.cos(angle / 2.0)
        b, c, d = -axis * np.sin(angle / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                        [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                        [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])'''
# SlowCube.py

from OpenGL.GL import *
import numpy as np
import math

_lightVector = np.asfarray([0,0,1, 0])

class SlowCube:
    def __init__(self, vertices, surfaces, color):
        '''self.verts = np.asfarray([( 1, -1, -1), 
                                  ( 1,  1, -1), 
                                  (-1,  1, -1), 
                                  (-1, -1, -1),
                                  ( 1, -1,  1),
                                  ( 1,  1,  1),
                                  (-1, -1,  1),
                                  (-1,  1,  1)])
        self.surfaces = np.array([(0,1,2,3),
                                 (3,2,7,6),
                                 (6,7,5,4),
                                 (4,5,1,0),
                                 (1,5,7,2),
                                 (4,0,3,6)])
        self.color = np.asfarray([0,0,1])'''
        self.verts, self.surfaces, self.color = np.asfarray(vertices), np.asfarray(surfaces), np.asfarray(color)
        self.normals = np.asfarray([(0,0,-1, 0),
                                   (-1,0,0, 0),
                                   (0,0,1, 0),
                                   (1,0,0, 0),
                                   (0,1,0, 0),
                                   (0,-1,0, 0)])
        self.ang = 0
        self.axis = (3,1,1)

    def Update(self, deltaTime):
        self.ang += 50.0 * deltaTime

    def _DrawBlock(self):
        global _lightVector

        m = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX))
        light = np.matmul(_lightVector, m)

        glBegin(GL_QUADS)
        for n, surface in enumerate(self.surfaces):
            for vert in surface:
                dotP = np.dot(light, self.normals[n])
                mult = max(min(dotP, 1), 0)
                glColor3fv(self.color * mult)
                glVertex3fv(self.verts[int(vert)])
        glEnd()

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glRotatef(self.ang, *self.axis) # * splits the contents
        self._DrawBlock()

        glLoadMatrixf(m)
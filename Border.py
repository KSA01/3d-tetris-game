
from OpenGL.GL import *
import numpy as np
import math

_verts = (( 4, -6, -4),
          ( 4,  6, -4),
          (-4,  6, -4),
          (-4, -6, -4),
          ( 4, -6,  4),
          ( 4,  6,  4),
          (-4, -6,  4),
          (-4,  6,  4)
          )

_lines = ((0,1,2,3,0,4,5,7,6,4), (5,1), (6,3), (7,2))

def Render():
    global _verts
    global _lines

    m = glGetDouble(GL_MODELVIEW_MATRIX)

    glBegin(GL_LINES)
    for line in _lines:
        for i in range(len(line)-1):
            glVertex3fv(_verts[line[i]])
            glVertex3fv(_verts[line[i+1]])
    glEnd()

    glLoadMatrixf(m)


#TODO: Camera works, but relative position must be set for camera and movement
#Rotates the camera 90 degrees in a direction (dir: 0 = up, 1 = down, 2 = left, 3 = right)
def rotateCamera(dir):
    if dir == 0:
        glRotate(30, 1, 0, 0)
    elif dir == 1:
        glRotate(-30, 1, 0, 0)
    elif dir == 2:
        glRotate(90, 0, 1, 0)
    elif dir == 3:
        glRotate(-90, 0, 1, 0)


    pass
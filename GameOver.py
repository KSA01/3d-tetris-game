#GameOver.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import UI

# screen size
width, height = 640, 750

def Render():
    # Setting up orthographic projection for text rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Render the text
    UI.render_text("Game Over", 80, 320, 42)

    # Restore the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
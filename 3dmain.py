# 3dmain.py
# orthographic view

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from SlowCube import SlowCube
#import Cube
import Pieces
import Border

pygame.init()
size = width, height = 640, 750
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glTranslate(1.0, 0.0, -30.0)     #translates the camera
glRotate(-15, 0, 1, 0)           #rotate -15 degrees around y
glRotate(30, 1, 0, 0)            #rotate 30 degrees around x

#Cube.Init()
#cube = Cube.Cube()
#cube = SlowCube()

tetrisPieces = Pieces.createTetrisPieces()
#print("NUM TETRIS PIECES: " + str(len(tetrisPieces)))

tetrisCubes = 0
for piece in tetrisPieces:
    tetrisCubes += len(piece.cubes)

#print("NUMBER OF CUBES: " + str(tetrisCubes))

def Update(deltaTime):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
    #cube.Update(deltaTime)
    for piece in tetrisPieces:
        piece.Update(deltaTime)

    return True

def Render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #cube.Render()
    for piece in tetrisPieces:
        piece.Render()

    Border.Render()

    pygame.display.flip()

_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render()
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t

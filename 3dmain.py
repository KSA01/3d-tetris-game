# 3dmain.py

import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from SlowCube import SlowCube
from SlowTriangle import SlowTriangle
import Cube
import Pieces
import Border
import GamePlay
import GameOver

#Camera
import Camera
#Camera

#Need to install for UI
from freetype import *
import pygame.freetype

pygame.init()
size = width, height = 640, 750
screen = pygame.display.set_mode(size, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width/height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

glTranslate(1.0, 0.0, -26.0)     #translates the camera
#glRotate(-15, 0, 1, 0)           #rotate -15 degrees around y
#glRotate(30, 1, 0, 0)            #rotate 30 degrees around x

GamePlay.Init()


_isPaused = False

#UI
triangle = SlowTriangle()
#UI

tetrisPieces = Pieces.createTetrisPieces()
#print("NUM TETRIS PIECES: " + str(len(tetrisPieces)))

tetrisCubes = 0
for piece in tetrisPieces:
    tetrisCubes += len(piece.cubes)

#print("NUMBER OF CUBES: " + str(tetrisCubes))

def Update(deltaTime):

    global _isPaused #Access the global pause variable

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Check if ESC key is pressed
            _isPaused = not _isPaused #Toggle the pause state
            if _isPaused:
                GamePlay.Pause() # Call a new function to handle pause in GamePlay
            else:
                GamePlay.Resume() # Call a new function to handle resume in GamePlay
            continue
        if _isPaused:
            continue # Skip the rest of the loop if the game is paused

        if GamePlay.ProcessEvent(event):
            continue
    
    GamePlay.Update(deltaTime, tetrisPieces)
    
    #Camera
    Camera.Update(deltaTime)

    #UI
    triangle.Update(deltaTime)
    #UI

    return True

def Render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    if not Pieces.CheckForCeil():  # Checks if any cubes have hit the ceiling
        GamePlay.Pause()
        GameOver.Render()

    #NEW
    #Render Border first so transparency works correctly
    Border.Render()

    GamePlay.Render()
    
    #UI TEST
    #triangle.Render()
    #UI
    

    pygame.display.flip()

_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render()
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t

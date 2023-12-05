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
import UI

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

glTranslate(1.0, 0.0, -25.0)     #translates the camera
glRotate(-15, 0, 1, 0)           #rotate -15 degrees around y
glRotate(30, 1, 0, 0)            #rotate 30 degrees around x

Cube.Init()
#cube = Cube.Cube()
#cube = SlowCube()
GamePlay.Init()

#ALFREDO
_isPaused = False
#ALFREDO

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
    #ALFREDO
    global _isPaused #Access the global pause variable
    #ALFREDO

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        #ALFREDO
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Check if ESC key is pressed
            _isPaused = not _isPaused #Toggle the pause state
            if _isPaused:
                GamePlay.Pause(tetrisPieces) # Call a new function to handle pause in GamePlay
            else:
                GamePlay.Resume(tetrisPieces) # Call a new function to handle resume in GamePlay
            continue
        if _isPaused:
            continue # Skip the rest of the loop if the game is paused
        #ALFREDO

        if GamePlay.ProcessEvent(event):
            continue

    #GamePlay.Update(deltaTime)

    #cube.Update(deltaTime)
    #for piece in tetrisPieces:
        #piece.Update(deltaTime)
    
    #BOOKMARK: This is where game loop checks for pause
    #ALFREDO
    #if not _isPaused: # Only update game state if not paused
    #ALFREDO
        #GamePlay.Update(deltaTime, tetrisPieces)

    
    GamePlay.Update(deltaTime, tetrisPieces)
    

    #UI
    triangle.Update(deltaTime)
    #UI

    return True

def Render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #NEW
    #Render Border first so transparency works correctly
    Border.Render()

    #cube.Render()
    for piece in tetrisPieces:
        #piece.Render()
        GamePlay.Render(piece)

    #GamePlay.Render()
    
    #UI
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

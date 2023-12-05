# GamePlay.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import random
import Pieces
import UI

icons = (
    "Icons/IIcon.png",
    "Icons/JIcon.png",
    "Icons/LIcon.png",
    "Icons/OIcon.png",
    "Icons/SIcon.png",
    "Icons/TIcon.png",
    "Icons/ZIcon.png"
)

def Init():
    global _piece
    #NEW
    global _nextPiece
    global nextIndex
    #NEW
    global OnStart
    global moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown

    Pieces.Init()
    OnStart = True
    moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown = False, False, False, False, False, False, False

def ProcessEvent(event):
    global moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown
    #add player key shift movements using arrow keys
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            moveLeft = True
        elif event.key == pygame.K_RIGHT:
            moveRight = True
        elif event.key == pygame.K_DOWN:
            moveDown = True
        elif event.key == pygame.K_UP:
            moveUp = True
        elif event.key == pygame.K_a:
            rotateLeft = True
        elif event.key == pygame.K_d:
            rotateRight = True
        elif event.key == pygame.K_s:
            rotateDown = True

    return False

index = random.randint(0, 6)
#NEW
#Get a random index for the next piece
nextIndex = random.randint(0, 6)
#NEW

#Set the next piece display
icon_idx = nextIndex

_isGamePaused = False  # A new global variable to track the pause state

def Pause(pieces):
    global _isGamePaused
    global _piece

    #Bandaid solution, commented out
    #_piece = pieces[index]

    _isGamePaused = True
    #TODO: When this function is called, trigger all cubes on screen to disappear (on final assignment)
    #Toggle current piece to disappear
    _piece.ToggleCubes(False, True)

def Resume(pieces):
    global _isGamePaused
    global _piece

    #Bandaid solution, commented out
    #_piece = pieces[index]

    _isGamePaused = False

    #TODO: When this function is called, trigger all cubes on screen to appear (on final assignment)
    #Toggle current piece to appear
    _piece.ToggleCubes(True, False)


def Update(deltaTime, pieces):
    global _piece
    global index
    #NEW
    global nextIndex
    global icon_idx
    #NEW
    global OnStart
    global moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown

    _piece = pieces[index]

    if OnStart:
        _piece.ResetCubePos()
        updatePos = (0, 6, -2)
        _piece.SetPos(updatePos)
        OnStart = False

        #NEW
        #Toggle cubes of piece to fade in
        _piece.ToggleCubes(True, False)


    # Check if piece hits the bottom
    move = np.asfarray([0, -8*deltaTime, 0])
    if move[1] + _piece.GetPos()[1] <= -5:

        #Update index to next index and grab a new next index
        index = nextIndex
        nextIndex = random.randint(0, 6)

        #Set the next piece display
        icon_idx = nextIndex

        OnStart = True
        move[1] += 24

    #Check if piece is close to bottom. If so, toggle cubes to fade
    if move[1] + _piece.GetPos()[1] <= -4:
        #Toggle cubes of piece to fade out
        _piece.ToggleCubes(False, True)

    # Check if piece is not at z limit then move
    if _piece.GetPos()[2] >= -4:
        if moveUp:
            move[2] += -2
            moveUp = False
    if _piece.GetPos()[2] <= 1.5:
        if moveDown:
            move[2] += 2
            moveDown = False

    # Check if piece is not at x limit then move
    if _piece.GetPos()[0] >= -3:
        if moveLeft:
            move[0] += -2
            moveLeft = False
    if _piece.GetPos()[0] <= 3:
        if moveRight:
            move[0] += 2
            moveRight = False

    # Rotate piece
    if rotateLeft:
        _piece.Rotate(90, (0, -2, 0))
        rotateLeft = False
    elif rotateRight:
        _piece.Rotate(-90, (0, -2, 0))
        rotateRight = False
    elif rotateDown:
        _piece.Rotate(-90, (-2, 0, 0))
        rotateDown = False

    _piece.Update(deltaTime, move, _isGamePaused)

#Probably shouldn't pass in anything here
def Render(piece):
    global _piece
    global icon_idx

    # screen size
    width, height = 640, 750

    # Setting up orthographic projection for text rendering
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, height, 0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    #Render the image
    UI.render_image(70, 50, 70, 100, image_path=icons[0])

    # Render the text
    UI.render_text("next", 50, 10, 48)

    # Restore the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    #_piece = piece #Commented out, this line was causing _piece to be set to Z every frame

    _piece.Render()
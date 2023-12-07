# GamePlay.py

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import random
import Pieces
import UI

#Camera
import Border
import Camera
#Camera

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

    #Camera
    global camUp, camDown, camLeft, camRight
    camUp, camDown, camLeft, camRight = False, False, False, False
    #Camera

    Pieces.Init()
    OnStart = True
    moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown = False, False, False, False, False, False, False

def ProcessEvent(event):
    global moveUp, moveDown, moveLeft, moveRight, rotateLeft, rotateRight, rotateDown
    
    #Camera
    global camUp, camDown, camLeft, camRight
    #Camera

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

    #Camera
        if event.key == pygame.K_i:
            camUp = True
        elif event.key == pygame.K_k:
            camDown = True
        elif event.key == pygame.K_j:
            camLeft = True
        elif event.key == pygame.K_l:
            camRight = True
    #Camera

    return False

index = random.randint(0, 6)
#NEW
#Get a random index for the next piece
nextIndex = random.randint(0, 6)
#NEW

#Set the next piece display
icon_idx = nextIndex

_isGamePaused = False  # A new global variable to track the pause state

def Pause():
    global _isGamePaused
    global _piece

    _isGamePaused = True
    #TODO: When this function is called, trigger all cubes on screen to disappear (on final assignment)
    #Toggle current piece to disappear
    _piece.ToggleCubes(False, True)

def Resume():
    global _isGamePaused
    global _piece

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

    #Camera
    global camUp, camDown, camLeft, camRight
    #Camera

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
    move = np.asfarray([0, -2*deltaTime, 0])
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


    #Camera-Relative Movement Update
    #BUG: Need proper out of bounds checks, movement doesn't always work after camera turns

    #Get the axis currently facing camera
    if moveUp or moveDown or moveLeft or moveRight:
        curSide = Camera.getCurSide()
        print(curSide)

    # Check if piece is not at z limit then move
    if _piece.GetPos()[2] >= -4:
        if moveUp:
            if curSide == 'z':
                move[2] += -2
            elif curSide == 'x':
                move[0] += 2
            elif curSide == '-z':
                move[2] += 2
            elif curSide == '-x':
                move[0] += -2
            moveUp = False
    if _piece.GetPos()[2] <= 1.5:
        if moveDown:
            if curSide == 'z':
                move[2] += 2
            elif curSide == 'x':
                move[0] += -2
            elif curSide == '-z':
                move[2] += -2
            elif curSide == '-x':
                move[0] += 2
            moveDown = False

    # Check if piece is not at x limit then move
    if _piece.GetPos()[0] >= -3:
        if moveLeft:
            if curSide == 'z':
                move[0] += -2
            elif curSide == 'x':
                move[2] += -2
            elif curSide == '-z':
                move[0] += 2
            elif curSide == '-x':
                move[2] += 2
            moveLeft = False
    if _piece.GetPos()[0] <= 3:
        if moveRight:
            if curSide == 'z':
                move[0] += 2
            elif curSide == 'x':
                move[2] += 2
            elif curSide == '-z':
                move[0] += -2
            elif curSide == '-x':
                move[2] += -2
            moveRight = False   





    #OLD CODE, NOT CAMERA-RELATIVE MOVEMENT (kept just in case)
    # Check if piece is not at z limit then move
    #if _piece.GetPos()[2] >= -4:
    #    if moveUp:
    #        move[2] += -2
    #        moveUp = False
    #if _piece.GetPos()[2] <= 1.5:
    #    if moveDown:
    #        move[2] += 2
    #        moveDown = False

    # Check if piece is not at x limit then move
    #if _piece.GetPos()[0] >= -3:
    #    if moveLeft:
    #        move[0] += -2
    #        moveLeft = False
    #if _piece.GetPos()[0] <= 3:
    #    if moveRight:
    #        move[0] += 2
    #        moveRight = False







    # Rotate piece
    if rotateLeft:
        _piece.ToggleRotate("left")
        #_piece.Rotate(90, (0, -2, 0))
        rotateLeft = False
    elif rotateRight:
        _piece.ToggleRotate("right")
        #_piece.Rotate(-90, (0, -2, 0))
        rotateRight = False
    elif rotateDown:
        _piece.ToggleRotate("down")
        #_piece.Rotate(-90, (-2, 0, 0))
        rotateDown = False

    _piece.Update(deltaTime, move, _isGamePaused)

    #Camera
    if camUp:
        #print("Cam up")
        Camera.toggleCamMove(0, 1)
        #Border.rotateCamera(0)
        camUp = False
    elif camDown:
        #print("Cam down")
        Camera.toggleCamMove(0, -1)
        #Border.rotateCamera(1)
        camDown = False
    elif camLeft:
        #print("Cam left")
        Camera.toggleCamMove(1, 0)
        #Border.rotateCamera(2)
        camLeft = False
    elif camRight:
        #print("Cam right")
        Camera.toggleCamMove(-1, 0)
        #Border.rotateCamera(3)
        camRight = False
    #Camera


def Render():
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
    UI.render_image(70, 50, 100, 100, image_path=icons[icon_idx])

    # Render the text
    UI.render_text("next", 50, 10, 48)

    # Restore the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    _piece.Render()